#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import sqlite3 as sqlite
from collections import defaultdict
from datetime import datetime
import glob
import os
import sys

# Two dicts, one sorted by product and one sorted by so
productDict = defaultdict(list)
soDict = defaultdict(list)
dellDict = defaultdict(list)
dellPODict = defaultdict(list)
dellDeliveredDict = defaultdict(list)


def loadDicts(state):
    productDict.clear()
    soDict.clear()
    ignoreDict = loadIgnoreDict(state)
    """
    Generic function to load CSV data into the two dicts
    Expect to run this every time you want data to update
    TODO: figure out what happens if we're writing at the same time we read
    """
    # Set locationGroupId based on state. Currently unused.
    match state:
        case "WA":
            stateId = '7'
        case "QLD":
            stateId = '1'
        case "SP":
            stateId = '2'
        case "VIC":
            stateId = '10'
        case "SILVER":
            stateId = '11'

    # Connect to exportDB
    try:
        conn = sqlite.connect('static/dbexport/dashboard.db', check_same_thread = False)
        conn.text_factory = lambda x: str(x, 'utf-8', 'ignore')
        conn.row_factory = sqlite.Row
        c = conn.cursor()
    except Exception as e:
        print("Error opening database")
        print(e)

    try:
        c.execute('SELECT * FROM '+ state +'Export;')
        ret = c.fetchall()

    except Exception as e:
        print(e)

    for row in ret:
        if checkIgnore(row['num'], row['productNum'], ignoreDict):
            continue
        if (row['num'] in ignoreDict.keys()):
            for line in ignoreDict[row['num']]:
                if (line['product'] == row['productNum']):
                    continue
        # Change SQLite3 row object into a dict
        row = dict(row)
        row['dateLastModified'] = row['dateLastModified'].split(" ")[0]
        row['dateLastModified'] = datetime.strptime(row['dateLastModified'], '%Y-%m-%d')
        productDict[row['productNum']].append(row)
        soDict[row['num']].append((row))


def filterproductDict(column, data, match=True):
    """
    Generic module to filter the sorted by product dict.
    Column can be any header we import. Data can be a string or a list
    of what to search for. Match is a "NOT" flag
    Example usage: filterproductDict('pickitemstatusId','5',True)
    Would search for all issued items not in stock
    """
    # We will return this dict of filtered data
    returnDict = defaultdict(list)
    # Iterate through the sorted dict & subdict to filter, then add that data to our filtered dict
    for product in productDict:
        # TODO: Error handling if there is a keyerror via someone typing 'column' incorrectly
        for subDict in productDict[product]:
            if match:
                if (subDict[column] in data):
                    returnDict[product].append(subDict)
            else:
                if (subDict[column] not in data):
                    returnDict[product].append(subDict)
    return returnDict


def filtersoDict(column, data, match=True):
    """
    Generic module to filter the sorted by so dict.
    Column can be any header we import. Data is what to search for. Match is a "NOT" flag
    Example usage: filtersoDict('pickitemstatusId','5',True) - Search for all issued items not in stock
    """
    # We will return this dict of filtered data
    returnDict = defaultdict(list)
    # Iterate through the sorted dict & subdict to filter, then add that data to our filtered dict
    for so in soDict:
        for subDict in soDict[so]:
            if match:
                if (subDict[column] in data):
                    returnDict[so].append(subDict)
            else:
                if (subDict[column] not in data):
                    returnDict[so].append(subDict)
    return returnDict


def committedDict(pickItemStatus):
    """
    Returns all orders that are committed in full
    Example usage: committedDict() - Search for all committed in full orders
    """
    # We will return this dict of filtered data
    returnDict = defaultdict(list)
    # Iterate through the sorted dict & subdict to filter, then add that data to our filtered dict
    for so in soDict:
        add = 0
        templist = []
        # TODO: Error handling if there is a keyerror via someone typing 'column' incorrectly
        for subDict in soDict[so]:
            if (subDict['pickitemstatusId'] == pickItemStatus):
                templist.append(subDict)
            elif (subDict['pickitemstatusId'] == ''):
                pass
            else:
                add = 1
        if add != 1:
            for i in templist:
                returnDict[so].append(i)
    return returnDict


# Return the full SO dict
def fullSoDict():
    return soDict


# Return the full Product dict
def fullProductDict():
    return productDict


# Add a row to the ignore list
def ignoreRow(row, date, state):
    rowlist = row.split(',')
    rowlist.append(date)
    rowlist.append(state)
    print("Rowlist*** " + str(rowlist) + "***END Rowlist")
    with open("static/dbexport/ignore.csv", mode='a+', newline='') as ignorecsv:
        csv_writer = csv.writer(ignorecsv)
        csv_writer.writerow(rowlist)


def loadIgnoreDict(state):
    ignoreDict = defaultdict(list)
    with open("static/dbexport/ignore.csv", newline='') as ignorecsv:
        ignoreReader = csv.DictReader(ignorecsv)
        for row in ignoreReader:
            if (datetime.strptime(row['date'], '%d/%m/%Y') > datetime.now()) and (row['state'] == state):
                ignoreDict[row['so']].append(row)
        return ignoreDict


def checkIgnore(so, productNum, ignoreDict):
    for row in ignoreDict[so]:
        if row['product'] == productNum:
            print(productNum + " was ignored for SO " + so)
            return True
    return False


def latestDellFile():
    """
    Generic function to identify the latest Dell export file
    """
    dellExport = 'static/dell/Orders*.csv'
    listOfFiles = glob.glob(dellExport)
    ret = max(listOfFiles, key=os.path.getctime) 
    return ret


def loadDell():
    dellDict.clear()
    """
    Generic function to load CSV data into the Dell dict
    Expect to run this every time you want Dell data to update
    """
    # Define which Dell Order CSV to open
    latestFile = latestDellFile()

    with open(latestFile, newline='') as csvfile:
        # Load CSV into a our reader module
        exportReader = csv.DictReader(csvfile)
        # Sort data by product and by so
        for row in exportReader:
            if row['Status'] != "Cancelled":
                dellDict[row['Dell Order Number']].append(row)
    return dellDict


def loadDellPODict(dellDict=loadDell()):
    dellPODict.clear()
    """
    Module to order the dellDict by VSP PO number, while filtering for only outstanding POs
    """
    for order in dellDict:
        if len(dellDict[order][0]['Actual Delivery Date']) == 0:
            dellPODict[dellDict[order][0]['Purchase Order Number']].append(dellDict[order])

    return dellPODict


def loadDellDeliveredDict(dellDict=loadDell()):
    dellDeliveredDict.clear()
    """
    Module to order the dellDict by VSP PO number, while filtering for only delivered POs
    """
    for order in dellDict:
        if len(dellDict[order][0]['Actual Delivery Date']) > 0:
            dellDeliveredDict[dellDict[order][0]['Purchase Order Number']].append(dellDict[order])

    return dellDeliveredDict
