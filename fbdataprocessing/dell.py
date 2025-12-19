#!/usr/bin/python
# -*- coding: utf-8 -*-

import fishpost
import dellpost
import configparser
import logging
import traceback
from emailSender import createMsgGeneric, sendEmail
import json
import time
import os

print(f"Starting dell.py at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
# Config
cfg = configparser.ConfigParser() #debugging
script_dir = os.path.dirname(os.path.abspath(__file__)) #debugging
config_path = os.path.join(script_dir, 'config.ini') #debugging
print(f"Looking for config at: {config_path}") #debugging

cfg.read('config.ini')
print(f"Sections found: {cfg.sections()}")
print(f"FB host: {cfg['FB']['host']}")


#Logs to DELLAPI.log in the script folder
logging.basicConfig(filename=cfg['SYSTEM']['writepath']+'DELL-PROCESSING.log',level=logging.INFO,format='%(asctime)s %(message)s')
def get_token():
    #Log in, acquire token, profit
    fb_token = None
    i = 0 #Number of times to attempt getting a token before we fail

    while i<5: #Loop over until we get a token
        i += 1 #Increment loop counter
        try:
            print(f"Requesting Token from Fishbowl, Attempt #: {i}")
            fb_token = fishpost.login(cfg['FB']['host'], cfg['FB']['appName'], cfg['FB']['appDescription'], cfg['FB']['appId'], cfg['FB']['username'], cfg['FB']['password'])
            return fb_token #once we successfully get a token we're good to exit
        except:
            logging.error(traceback.format_exc())
            print("Failed to get token.")
            time.sleep(10)
    if not fb_token:
        logging.error("Could not log into Fishbowl after 5 attempts. Exiting.")
        return


def main():
    print("Syncing Dell Order Status")
    fb_orders = []
    fb_host = cfg['FB']['host']
    fb_token = get_token()
    print(f"Acquired token {fb_token}")
    print(f"Using Fishbowl IP {fb_host}")
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
        print(f"About to send query to: {fb_host}") #more debugging - cronjob isn't working
        fb_req = fishpost.dataQuery(fb_host, fb_token, sql)
        print(f"Request headers: {fb_req.request.headers}") #more debugging
        print(f"Sending Fishbowl Request, received back {fb_req.text}") #more debugging
        fb_orders = json.loads(fb_req.text)
    except:
        logging.error(traceback.format_exc())
        print("Error: Could not parse Fishbowl response as JSON. Exiting.")
        fishpost.logout(fb_host, fb_token)
        return

    # Check if the response is an API error message
    if isinstance(fb_orders, dict) and fb_orders.get('status') != 200:
        error_message = fb_orders.get('message', 'Unknown API Error.')
        print(f"Fishbowl API Query Failed (Status {fb_orders.get('status')}): {error_message}")
        print("Exiting due to Fishbowl API error.")
        fishpost.logout(fb_host, fb_token)
        return

    if not fb_orders:
        print("No open Dell PO Items found in Fishbowl or data query returned empty.")
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
        print("Could not log into Dell.")
        fishpost.logout(fb_host, fb_token)
        return

    BATCH_SIZE = 10 #Dell imposes a limit of 10 PO numbers per API call
    all_dell_orders = [] #List of all our results
    
    search_url = cfg['DELL'].get('search_url')
        
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
    cancelled_po_list = [] #Keep track of any POs that are listed as cancelled in Dell's Order API

    for dell_order in dell_orders_list:
        dell_po_num = dell_order['purchaseOrderNumber']
        
        # Calculate longest lead time (because we can't know which item is which)
        max_eta_resp = dellpost.get_max_eta(dell_order) #returns a dict of two values: the highest ETA, and some info for notes field
        max_eta = max_eta_resp['max_eta']
        notes = max_eta_resp['notes']

        #Check if the order is cancelled and still exists in our list of issued POs
        if notes == "Cancelled" and dell_po_num in po_numbers_list: 
            cancelled_po_list.append(dell_po_num)

        #Check if the Dell PO is in the list of Fishbowl POs. If it is, remove it from our list.
        #At the end of the file, the remaining PO numbers will be emailed as an alert to the Dell PM
        try:
            po_numbers_list.remove(dell_po_num)
        except ValueError as e:
            print("Couldn't find Fishbowl PO to match")
            logging.error(f"Error on matching Dell PO to Fishbowl: {e}")

        if max_eta and dell_po_num in po_map:
            new_date_str = max_eta.strftime('%Y-%m-%dT00:00:00.000+10')
            
            po_data = po_map[dell_po_num]
            po_id = po_data['po_id'] #Save ID for later, we have to strip it out to send the response

            po_response = fishpost.loadObject(fb_host, fb_token, "purchase-orders", po_id)
            
            if po_response.status_code != 200:
                print(f"Failed to load PO {dell_po_num} with response code {po_response.status_code}")
                logging.error(f'Failed to load PO, got response: {po_response.status_code}')
                continue
                
            po_obj = po_response.json()
            
            # Only bother updating if we actually get a response
            if po_obj and 'dateScheduled' in po_obj:
                
                # Check if date needs updating
                if po_obj:#['dateScheduled'][:10] != new_date_str[:10]:
                    #Update Date Scheduled (top of PO)
                    #Remove the check condition so we update status all the time
                    old_date_str = po_obj['dateScheduled']
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

                    print(f"Updating: PO {dell_po_num}")
                    print(f"Old Date: {old_date_str}")
                    print(f"New Date: {new_date_str}")
                    
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

    #Send email with remaining PO numbers to Dell PM
    if po_numbers_list: #Check if any POs are left in Fishbowl that don't have a matching Dell Order Placed
        try:       
            sendEmail(
                createMsgGeneric(
                    "Error: Dell POs haven't been placed", #Subject
                    "tom@vspsolutions.com.au", #From: Email Address
                    "dell@vspsolutions.com.au", #To: Email Address
                    f"The following POs haven't been placed: {po_numbers_list}" #Email body
                    )
                )
            print(f"Sent email warning that POs {po_numbers_list} weren't showing in Dell's Order Status")
        except Exception as e:
            logging.error(f"Error sending email for missing POs: {e}")

    if cancelled_po_list:
        #Send email alerting if we have cancelled orders in Dell's Order Status
        #POs must be still issued in Fishbowl
        ###
        try:
            sendEmail(
            createMsgGeneric(
                "Error: Dell POs have been cancelled", #Subject
                "tom@vspsolutions.com.au", #From: Email Address
                "dell@vspsolutions.com.au", #To: Email Address
                f"The following POs have been cancelled: {cancelled_po_list}" #Email body
                )
            )
            print(f"Sent email warning that POs {cancelled_po_list} are showing as cancelled")
        except Exception as e:
            logging.error(f"Error sending email for cancelled POs: {e}")
    print("Finish")

if __name__ == "__main__":
    main()