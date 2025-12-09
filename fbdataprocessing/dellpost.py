#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from dateutil import parser

def get_token(url, client_id, client_secret):
    #
    #Authenticates with Dell's API endpoint and returns the Access Token.
    ###

    postData = {
        'grant_type': 'client_credentials', 
        'client_id': client_id, #Set in config.ini
        'client_secret': client_secret #Set in config.ini
    }
    
    try:
        req = requests.post(url, data=postData, timeout=10)
        req.raise_for_status() # Raises error for 400/500 codes
        return req.json().get('access_token')
    except Exception as e:
        print(f"Dell Auth Error: {e}")
        return None

def search_orders(url, token, po_numbers):
    #
    #Searches for a list of PO numbers.
    #po_numbers: A list of strings, e.g., ['1001', '1002']
    ###

    head = {'Authorization': "Bearer " + token, 'Content-Type': 'application/json'} #Set headers
    
    #FYI Dell API has a limit of 10 values at once
    data = {"searchParameter": [{"key": "po_numbers", "values": po_numbers}]}

    try:
        req = requests.post(url, headers=head, json=data, timeout=30)
        req.raise_for_status()
        return req.json()
    except requests.exceptions.HTTPError as e:
        print(f"Dell API Error: {e}")
        return None

def get_max_eta(dell_order):
    """
    Parses a single Dell Order object.
    Loops through all line items to find the furthest 'estimatedDeliveryDate'.
    Returns: A datetime object or None.
    """
    dates = []
    notes = ""
    ret = {}
    
    #Iterate through each line - each Dell PO can have multiple line items
    for line in dell_order['dellOrders']:
        #Check dates and grab the one that is most relevant. Actual > Revised > Estimated
        if(line['actualDeliveryDate']):
            dt = parser.parse(line['actualDeliveryDate'])
        elif(line['revisedDeliveryDate']):
            dt = parser.parse(line['revisedDeliveryDate'])
        else:
            dt = parser.parse(line['estimatedDeliveryDate'])
        dates.append(dt)
        notes = notes + "\n" + line['orderStatus']    
    if not dates:
        return None
        
    # Return the maximum (furthest) date found
    ret['max_eta'] = max(dates)
    ret['notes'] = notes
    return ret