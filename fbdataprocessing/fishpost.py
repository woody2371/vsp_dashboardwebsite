# Fishpost
# Python tool to simplify interacting with Fishbowl's REST API

import requests

#Set this to the URL of your Fishbowl webserver
url = 'http://10.62.20.114:88/api/'

#Authenticate with Fishbowl - first time you will need to navigate to Integrations and accept the integration
def login(appName, appDescription, appId, username, password):
	#Usage: login("FishbowlDashboardv2", "Fishbowl Integration based on REST API", 2371, "admin", "admin")
	#
	#Create json data packet for POST request, based on the data passed to the function
	postData = {'appName': appName, 'appDescription': appDescription, 'appId': appId, 'username': username, 'password': password}
	#Define the API URL
	reqURL = url + "login"
	#Create post request
	req = requests.post(reqURL, json = postData)
	#Print the response message from Fishbowl WEB API
	return req .json()['token']

def logout(token):
	#Usage: logout(token) where token is the returned value from login()
	#
	#Set the header for authentication
	head = {'Authorization': "Bearer " + token}
	#Define the API URL
	reqURL = url + "logout"
	#Create post request
	req = requests.post(reqURL, headers = head)
	#Print the response message from Fishbowl WEB API
	print(req.text)

def data-query():
	#Usage:
	#
	#Execute a query contained in the Data section of Fishbowl Reporting
	postData = {'appName': appName, 'appDescription': appDescription, 'appId': appId, 'username': username, 'password': password}
	#Define the API URL
	reqURL = url + "login"
	#Create post request
	req = requests.post(reqURL, json = postData)
	#Print the response message from Fishbowl WEB API
	return req .json()['token']



###EXAMPLE USAGE###

#Log in to Fishbowl, returning the authorization token for later usage
#token = login("FishbowlDashboardv2", "Fishbowl Integration based on REST API", 2371, "admin", "admin")

#Logout from Fishbowl
#logout(token)
