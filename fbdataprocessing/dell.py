#!/usr/bin/python
# -*- coding: utf-8 -*-
#Processing package for interpreting ChannelOrders.zip, which is exported from the Dell Premier Order Status page
#Intended to provide useable data for future use

import os
import glob
import csv
from collections import defaultdict
import configparser

#Config
cfg = configparser.ConfigParser()
cfg.read('config.ini')

#Old Config
dellExport = 'static/dell/Orders*.csv'
poExport = 'static/dell/WADashboardDELL.csv'

#Load the latest Dell Order spreadsheet
listOfFiles = glob.glob(dellExport) # * means all if need specific format then *.csv
latestFile = max(listOfFiles, key=os.path.getctime)

"""
Most of this file is identical to processcsv.py as the process is similar

Columns we care about in the Dell Order Dict:
Purchase Order Number
Service Tag

POItemStatus info:
10	Entered
20	Picking
30	Partial
40	Picked
45	Shipped
50	Fulfilled
60	Closed Short
70	Void
95	Historical

"""
orderDict = defaultdict(list)
poDict = defaultdict(list)
joinedDict = defaultdict(list)
checkPODict = {}

#Load Dell Order Summary CSV
def loadOrderDicts():
    orderDict.clear()
    with open(latestFile, newline='') as csvfile:
        # Load CSV into a our reader module
        exportReader = csv.DictReader(csvfile)
        # Sort data by product and by key
        for key, row in enumerate(exportReader):
            row['key'] = key
            orderDict[row['key']].append(row)

#Load Fishbowl PO Data Export CSV
def loadPODicts():
    poDict.clear()
    with open(poExport, newline='') as csvfile:
        # Load CSV into a our reader module
        exportReader = csv.DictReader(csvfile)
        # Sort data by product and by so
        for key, row in enumerate(exportReader):
            row['key'] = key
            poDict[row['key']].append(row)

#Load a joined dictionary comparing values from the Order CSV and the PO CSV
def loadJoinedDicts():
    #Load prereq dicts
    loadOrderDicts()
    loadPODicts()
    
    #Start template for joinedDict is PODict
    joinedDict = poDict

    #Iterate through poDict and append with info from OrderDict
    for key in joinedDict:
        #joinedDict[key][0][]
        return

#Verify that all POs in the system have been placed and that all Orders have a PO
def checkPO():
    loadPODicts()
    loadOrderDicts()

    #Create a list of all POs that are in Fishbowl
    for key in poDict:
        if int(poDict[key][0]['qtyRemaining']) > 0:
            checkPODict[poDict[key][0]['num']] = ""

    #Check the Order List against the previously created PO List
    for key in orderDict:
        try:
            checkPODict[orderDict[key][0]['Purchase Order Number']] = orderDict[key][0]['Dell Order Number']
        except:
            checkPODict["Error, Dell Order #: "+orderDict[key][0]['Dell Order Number']] = "Error"

    #Create a simple list of all errors to look at
    errorList = []
    for key in checkPODict:
        if checkPODict[key] == "" or checkPODict[key] == "Error":
            errorList.append(key)

    return errorList

def filterOrderDict(column, data, match=True):
    """
    Generic module to filter the sorted by product dict.
    Column can be any header we import. Data can be a string or a list of what to search for. Match is a "NOT" flag
    Example usage: filterproductDict('pickitemstatusId','5',True) - Search for all issued items not in stock
    """
    # We will return this dict of filtered data
    returnDict = defaultdict(list)
    # Iterate through the sorted dict & subdict to filter, then add that data to our filtered dict
    for product in productDict:
        # TODO: Error handling if there is a keyerror via someone typing 'column' incorrectly
        for subDict in productDict[product]:
            if match:
                if(subDict[column] in data):
                    returnDict[product].append(subDict)
            else:
                if(subDict[column] not in data):
                    returnDict[product].append(subDict)
    return returnDict

def fetchOrders():
    """
    Module to fetch all current Dell orders using the Dell OrderStatus API.
    Requires Dell client_id and client_secret to be configured in config.ini
    """
    client_id = cfg['DELL']['client_id']
    client_id = cfg['DELL']['client_secret']