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
            if(row['qty'] == ''):
                row['qty'] = '0'
            row['qty'] = int(row['qty'])
            row['dateLastModified'] = datetime.strptime(row['dateLastModified'], '%d/%m/%Y')
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
                    returnDict[product].append(subDict)
            else:
                if(subDict[column] not in data):
                    returnDict[product].append(subDict)

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
            else:
                add = 1
        if add != 1:
            for i in templist:
                returnDict[so].append(i)
    return returnDict

def fullSoDict():
    return soDict
    

loadDicts()
