#!/usr/bin/python
# -*- coding: utf-8 -*-

# Fishpost
# Python tool to simplify interacting with Fishbowl's REST API

import requests

#This URL is set in config.ini
#url = 'http://10.62.20.114:88/api/'

#Authenticate with Fishbowl - first time you will need to navigate to Integrations and accept the integration
def login(url, appName, appDescription, appId, username, password):
	#Usage: login("FishbowlDashboardv2", "Fishbowl Integration based on REST API", 2371, "admin", "admin")
	#
	###Log into Fishbowl###

	#Create json data packet for POST request, based on the data passed to the function
	postData = {'appName': appName, 'appDescription': appDescription, 'appId': appId, 'username': username, 'password': password}
	#Define the API URL
	reqURL = url + "login"
	#Create post request
	req = requests.post(reqURL, json = postData, timeout=10)
	#Print the response message from Fishbowl WEB API
	return req .json()['token']

def logout(url, token):
	#Usage: logout(token) where token is the returned value from login()
	#
	###Log out from Fishbowl###

	#Set the header for authentication
	head = {'Authorization': "Bearer " + token}
	#Define the API URL
	reqURL = url + "logout"
	#Create post request
	req = requests.post(reqURL, headers = head)
	#Print the response message from Fishbowl WEB API
	print(req.text)

def dataQuery(url, token, sql):
	#Usage: token is the returned value from login(), sql is a SQL query written to be compatible with Fishbowl's SQL query system
	#
	###Execute a SQL query, and return the data###

	#Set the header for authentication
	head = {'Authorization': "Bearer " + token, 'Content-Type': 'application/sql'}
	#Example SQL Query
	#sql = 'select * from soitem'
	#Define the API URL
	reqURL = url + "data-query"

	#Create GET request, passing the SQL request. Timeout set at 10s due to the large quantity of data we can sometimes pull
	req = requests.get(reqURL, headers = head, data = sql, timeout = 60)

	#Return the response message from Fishbowl's data query
	return req

def loadObject(url, token, module, obj_id):
    #Usage: token is the returned value from login(), module is which Fishbowl module to use, obj_id is the search term
    #
    #Example: loadObject(url, token, 'purchase-orders', '77913')
    ###Retrieve an object from Fishbowl

	#Debug
    print(f"Loading PO ID {obj_id}")
    #Set header for authentication
    head = {'Authorization': "Bearer " + token}
    
	#Define the API url
    reqURL = f"{url}{module}/{obj_id}"
    
	#Create the GET request, passing our URL above
    req = requests.get(reqURL, headers=head, timeout=10)

    return req

def saveObject(url, token, module, data_obj, id):
    #Set header for authentication
    head = {'Authorization': "Bearer " + token, 'Content-Type': 'application/json'}
    #Define the API url
    reqURL = f"{url}{module}/{id}"
    
    payload = data_obj.copy()
    payload.pop('id', None) #Remove ID - seems to cause issues??
    req = requests.post(reqURL, headers=head, json = data_obj, timeout=10)
    
    if req.status_code == 200:
        return True
    else:
        print(f"Error Saving Object: Status {req.status_code}")
        print(f"Response: {req.text}")
        return False
    
###EXAMPLE USAGE###

#Log in to Fishbowl, returning the authorization token for later usage
#token = login("FishbowlDashboardv2", "Fishbowl Integration based on REST API", 2371, "admin", "admin")

#Logout from Fishbowl
#logout(token)