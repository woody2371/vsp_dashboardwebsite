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
	req = requests.post(reqURL, json = postData)
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
	req = requests.get(reqURL, headers = head, data = sql, timeout = 10)

	#Return the response message from Fishbowl's data query
	return req


###EXAMPLE USAGE###

#Log in to Fishbowl, returning the authorization token for later usage
#token = login("FishbowlDashboardv2", "Fishbowl Integration based on REST API", 2371, "admin", "admin")

#Logout from Fishbowl
#logout(token)