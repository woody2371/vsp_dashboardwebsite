#!/usr/bin/python
# -*- coding: utf-8 -*-

import fishpost
import dellpost
import configparser
import logging
import traceback
import json
from dellpost import get_max_eta

# Config
cfg = configparser.ConfigParser()
cfg.read('config.ini')

logging.basicConfig(filename=cfg['SYSTEM']['writepath']+'DELLAPI.log',level=logging.DEBUG,format='%(asctime)s %(message)s')

def main():
    print("Syncing Dell Order Status")
    fb_token = None
    fb_host = None
    fb_orders = []

    #Log in, get token for later
    try:
        fb_host = cfg['FB']['host']
        fb_token = fishpost.login(cfg['FB']['host'], cfg['FB']['appName'], cfg['FB']['appDescription'], cfg['FB']['appId'], cfg['FB']['username'], cfg['FB']['password'])
    except:
        logging.error(traceback.format_exc())

    if not fb_token:
        logging.error("Could not log into Fishbowl. Exiting.")
        return

    #SQL Query - Can also use a Data Query inside Fishbowl's Data tab
    sql = """
        SELECT 
            po.id AS po_id,
            po.num,
            poitem.id AS poitem_id,
            poitem.dateScheduledFulfillment
        FROM po
        JOIN vendor ON po.vendorId = vendor.id
        JOIN poitem ON po.id = poitem.poId 
        WHERE po.statusId IN (20, 30)
        AND vendor.name LIKE 'Dell%'
    """
    
    try:
        fb_req = fishpost.dataQuery(fb_host, fb_token, sql)
        fb_orders = json.loads(fb_req.text)
    except:
        logging.error(traceback.format_exc())
        print("Error: Could not parse Fishbowl response as JSON. Exiting.")
        fishpost.logout(fb_host, fb_token)
        return

    # Check if the response is an API error message
    if isinstance(fb_orders, dict) and fb_orders.get('status', 200) != 200:
        error_message = fb_orders.get('message', 'Unknown API Error.')
        print(f"Fishbowl API Query Failed (Status {fb_orders.get('status')}): {error_message}")
        print("Exiting due to Fishbowl API error.")
        fishpost.logout(fb_host, fb_token)
        return

    if not fb_orders:
        print("No open Dell PO Items found in Fishbowl or data query returned empty. Exiting.")
        fishpost.logout(fb_host, fb_token)
        return

    po_map = {}
    for item in fb_orders:
        po_num = item['num']
        
        if po_num not in po_map:
            po_map[po_num] = {'po_id': item['po_id'], 'items': []}
        
        po_map[po_num]['items'].append({
            'poitem_id': item['poitem_id'],
        })

    po_numbers_list = list(po_map.keys())
    print(f"Found {len(po_numbers_list)} Purchase Orders ({len(fb_orders)} total items) to check.")

    try:
        dell_client_id = cfg['DELL']['client_id']
        dell_client_secret = cfg['DELL']['client_secret']
        auth_url = cfg['DELL']['auth_url']
        
        dell_token = dellpost.get_token(auth_url, dell_client_id, dell_client_secret)

    except Exception as e:
        print(f"Error during Dell login: {e}")
        fishpost.logout(fb_host, fb_token)
        return

    if not dell_token:
        print("Could not log into Dell. Exiting.")
        fishpost.logout(fb_host, fb_token)
        return

    BATCH_SIZE = 10 #Dell imposes a limit of 10 PO numbers per API call
    all_dell_orders = [] #List of all our results
    
    search_url = cfg['DELL'].get('search_url')
    
    if not po_numbers_list: #Check if somehow we have no Dell POs
        print("No POs to check.")
        fishpost.logout(fb_host, fb_token)
        return
        
    print("Querying Dell Order Status")

    #Run each batch API call
    for i in range(0, len(po_numbers_list), BATCH_SIZE):
        batch = po_numbers_list[i:i + BATCH_SIZE]
        batch_num = (i // BATCH_SIZE) + 1
        
        try:
            #Call Dell API for order status of all 10 PO numbers
            dell_req = dellpost.search_orders(search_url, dell_token, batch)
            all_dell_orders.extend(dell_req['purchaseOrderDetails'])
            print(f"Batch {batch_num} successful. Found {len(dell_req['purchaseOrderDetails'])} orders.")

        except Exception as e:
            print(f"API Error {e}")
            logging.error(f"Error on Batch {batch_num}: {e}")
            
    #Collect results
    dell_results = {'purchaseOrderDetails': all_dell_orders}

    if not dell_results:
        print("No data returned from Dell")
        fishpost.logout(fb_host, fb_token)
        return

    print("Updating Fishbowl")
    
    dell_orders_list = dell_results['purchaseOrderDetails']

    for dell_order in dell_orders_list:
        dell_po_num = dell_order['purchaseOrderNumber']
        
        # Calculate longest lead time (because we can't know which item is which)
        max_eta_resp = get_max_eta(dell_order) #returns a dict of two values: the highest ETA, and some info for notes field
        max_eta = max_eta_resp['max_eta']
        notes = max_eta_resp['notes']
        
        if max_eta and dell_po_num in po_map:
            new_date_str = max_eta.strftime('%Y-%m-%dT00:00:00.000+10')
            
            po_data = po_map[dell_po_num]
            po_id = po_data['po_id'] #Save ID for later, we have to strip it out to send the response

            po_response = fishpost.loadObject(fb_host, fb_token, "purchase-orders", po_id)
            
            if po_response.status_code != 200:
                print(f"Failed to load PO {dell_po_num}")
                continue
                
            po_obj = po_response.json()
            
            # Only bother updating if we actually get a response
            if po_obj and 'dateScheduled' in po_obj:
                
                # Check if date needs updating
                if po_obj:#['dateScheduled'][:10] != new_date_str[:10]:
                    #Update Date Scheduled (top of PO)
                    po_obj['dateScheduled'] = new_date_str
                    
                    #Sync line items - even though we don't really know their ETAs
                    if 'poItems' in po_obj:
                        for item in po_obj['poItems']:
                            if 'dateScheduled' in item:
                                item['dateScheduled'] = new_date_str
                    
                    #Fishbowl is funny about us sending read-only fields
                    read_only_fields = [
                        'id',
                        'status',           
                        'type',             
                        'lastModified',     
                        'issuedByUser',     
                        'dateCreated',             
                        'revisionNumber'
                    ]
                    
                    for field in read_only_fields:
                        po_obj.pop(field, None)
                    #Update the notes section to show the latest information about ETA
                    po_obj['note'] = f"Latest Dell Order Status: {notes}"

                    #Same but for poitems
                    if 'poItems' in po_obj:
                        for item in po_obj['poItems']:
                            item.pop('id', None)
                            item.pop('quantityFulfilled', None)  
                            item.pop('quantityPicked', None)     
                            item.pop('status', None)             
                    
                    print(f"Updating PO {dell_po_num} scheduled date to {new_date_str}")
                    
                    #Save PO
                    if po_obj['number']:
                        print(f"Saving PO {dell_po_num}...")
                        success = fishpost.saveObject(fb_host, fb_token, "purchase-orders", po_obj, po_id)
                        if not success:
                            print(f"Error saving PO {dell_po_num}")
                            logging.error(f"Failed to save PO {dell_po_num}")
                        else:
                            print(f"Successfully updated PO {dell_po_num}")
                else:
                    print(f"PO {dell_po_num} already up to date (scheduled: {po_obj['dateScheduled'][:10]}).")
            else:
                print(f"Failed to load PO {dell_po_num} or missing required fields.")
        else:
            print(f"Skipping PO {dell_po_num} (No ETA or not found in Fishbowl)")
            
    fishpost.logout(fb_host, fb_token)
    print("Finish")

if __name__ == "__main__":
    main()