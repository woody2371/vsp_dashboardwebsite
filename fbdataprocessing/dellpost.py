#!/usr/bin/python
# -*- coding: utf-8 -*-

# Python tool to simplify interacting with Dell's API 3.0
# More details can be found here: https://developer.dell.com/apis/bea0b0d7-239f-4ee7-b3ff-6ffe6c35ccc4/versions/3.0.0/Order_Status_Pull_API_3.0.0.json

import requests

#Send ID & Secret to Dell to obtain OAuth Token
def getOAuth(url, grant_type, client_id, client_secret):
    #Usage: 
    ###Send ID & Secret to Dell###

    #Create json data packet for POST request, based on the data passed to the function
	#Supported values for grant_type are: "client_credentials", "password"
	postData = {'grant_type': grant_type, 'client_id': client_id, 'client_secret': client_secret}
	#Create post request
	req = requests.post(url, data= postData, timeout=10)
	#Print the response message from Dell API
	#Expected response is access_token, token_type, expires_in, scope
	return req .json()

def orderStatusSearch(url, token, key, values):
	#Usage: token is the returned value from login(), key is what to search by, values is a list of values to search
	#Possible values:
	#
	###Execute a search by key, and return the data###

	#Set the header for authentication
	head = {'Authorization': "Bearer " + token, 'Content-Type': 'application/json'}
	###Example ###
	#key = 'po_numbers'
	#values = ['61576', '70576']
	data = {"SearchParameter": [{"key": key, "values": values }]}

	#Create POST request, passing the Search Parameters. Timeout set at 30s due to the large quantity of data we can sometimes pull
	req = requests.post(url, headers = head, json = data, timeout = 30)

	#Return the response message from Dell
	return req

###EXAMPLE USAGE###

#token = getOAuth('https://apigtwb2c.us.dell.com/auth/oauth/v2/token', 'client_credentials', 'client_id_here', 'client_secret_here')
#results = orderStatusSearch('https://apigtwb2c.us.dell.com/PROD/order-status/api/search', token['access_token'], 'po_numbers', ['70417', '68789', '12365'])