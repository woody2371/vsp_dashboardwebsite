#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
from collections import defaultdict
from datetime import datetime

# Two dicts, one sorted by product and one sorted by so
productDict = defaultdict(list)
soDict = defaultdict(list)

def loadDicts():
    productDict.clear()
    soDict.clear()
    ignoreDict = loadIgnoreDict()
    """
    Generic function to load CSV data into the two dicts
    Expect to run this every time you want data to update
    TODO: figure out what happens if we're writing at the same time we read
    """
    with open("static/dbexport/export.csv", newline='') as csvfile:
        # Load CSV into a our reader module
        exportReader = csv.DictReader(csvfile)
        # Sort data by product and by so
        for row in exportReader:
            if checkIgnore(row['num'], row['productNum'], ignoreDict):
                continue
            if(row['num'] in ignoreDict.keys()):
                for line in ignoreDict[row['num']]:
                    if(line['product'] == row['productNum']):
                        continue
            #No quantity returns null instead of zero - that doesn't work for displaying on a webpage
            if(row['qty'] == ''):
                row['qty'] = '0'
            if(row['qtyonhand'] == ''):
                row['qtyonhand'] = '0'
            #Qty for some reason is to 5 decimal places, we can't have half a camera.
            row['qty'] = int(float(row['qty']))
            row['qtyonhand'] = int(float(row['qtyonhand']))
            #Pull just the date, don't care about time
            row['dateLastModified'] = (row['dateLastModified'].split(" "))[0]
            #Turn date into an actual datetime object
            row['dateLastModified'] = datetime.strptime(row['dateLastModified'], '%Y-%m-%d')
            #Error checking - Fishbowl is really bad at knowing whether items are short or not
            if (row['pickitemstatusId']) == '5':
                if(row['qtyonhand'] >= row['qty']):
                    row['pickitemstatusText'] = "Ready to Pick"
                    row['pickitemstatusId'] = '10'
                    
            elif ((row['pickitemstatusId']) == '10') or ((row['pickitemstatusId']) == '11'):
                if(row['qtyonhand'] < row['qty']):
                    row['pickitemstatusText'] = "Short"
                    row['pickitemstatusId'] = '5'
            #Turn status codes into readable english
            if (row['pickitemstatusId']) == '5':
                row['pickitemstatusText'] = "Short"
            elif (row['pickitemstatusId']) == '6':
                    row['pickitemstatusText'] = "Hold"
            elif (row['pickitemstatusId']) == '10':
                row['pickitemstatusText'] = "Ready to Pick"
            elif (row['pickitemstatusId']) == '11':
                row['pickitemstatusText'] = "Ready to Pick"
            elif (row['pickitemstatusId']) == '20':
                row['pickitemstatusText'] = "Pick Started"
            elif (row['pickitemstatusId']) == '30':
                row['pickitemstatusText'] = "Committed"
            elif (row['pickitemstatusId']) == '40':
                row['pickitemstatusText'] = "Finished"
            else:
                #Catchall - not sure this is even required but at this point I don't trust fishbowl
                row['pickitemstatusText'] = "Unknown"
            productDict[row['productNum']].append(row)
            soDict[row['num']].append(row)

def filterproductDict(column, data, match=True):
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
        # TODO: Error handling if there is a keyerror via someone typing 'column' incorrectly
        for subDict in soDict[so]:
            if match:
                if(subDict[column] in data):
                    returnDict[so].append(subDict)
            else:
                if(subDict[column] not in data):
                    returnDict[so].append(subDict)
    return returnDict

def committedDict():
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
            if(subDict['pickitemstatusId']=='30'):
                templist.append(subDict)
            elif(subDict['pickitemstatusId']==''):
                pass
            else:
                add = 1
        if add != 1:
            for i in templist:
                returnDict[so].append(i)
    return returnDict

#Return the full SO dict
def fullSoDict():
    return soDict

#Return the full Product dict
def fullProductDict():
    return productDict

#Add a row to the ignore list
def ignoreRow(row,date):
    rowlist = row.split(',')
    rowlist.append(date)
    with open("static/dbexport/ignore.csv", mode='a+', newline='') as ignorecsv:
        csv_writer = csv.writer(ignorecsv)
        csv_writer.writerow(rowlist)

def loadIgnoreDict():
    ignoreDict = defaultdict(list)
    with open("static/dbexport/ignore.csv", newline='') as ignorecsv:
        ignoreReader = csv.DictReader(ignorecsv)
        for row in ignoreReader:
            if datetime.strptime(row['date'], '%d/%m/%Y') > datetime.now():
                ignoreDict[row['so']].append(row)
        return ignoreDict

def checkIgnore(so, productNum, ignoreDict):
    for row in ignoreDict[so]:
        if row['product'] == productNum:
            print(productNum + " was ignored for SO " + so)
            return True
    return False

