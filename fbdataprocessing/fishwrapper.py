#!/usr/bin/python
# -*- coding: utf-8 -*-
import struct
import configparser
import logging
import traceback
import pandas as pd
import fishpost
import json
import sqlite3

from statuscodes import getstatus
import queries

cfg = configparser.ConfigParser()
cfg.read('config.ini')

logging.basicConfig(filename=cfg['SYSTEM']['writepath']+'FBAPI.log',level=logging.DEBUG,format='%(asctime)s %(message)s')

# global functions
def xmlparse(xml):
	""" global function for parsing xml """
	root = etree.fromstring(xml)
	return root

def startExport (states=['WA','QLD','NSW','VIC']):
	print("Starting Data Import")
	try:
		#Log into Fishbowl and return auth token
		print("Logging in")
		token = fishpost.login(cfg['FB']['host'], cfg['FB']['appName'], cfg['FB']['appDescription'], cfg['FB']['appId'], cfg['FB']['username'], cfg['FB']['password'])
		print("Logged in")
		#Download per state:
		for state in states:
			#Download data - SQL query can be modified in config file
			print("Downloading data for {}".format(state))
			dataReturn = fishpost.dataQuery(cfg['FB']['host'], token, queries.query[state])
			print("Data downloaded for {}".format(state))
			#Move data to a pandas dataframe
			df = pd.json_normalize(json.loads(dataReturn.text))
			#Write data to CSV
			df.to_csv(cfg['SYSTEM']['XMLwritepath']+'{}export.csv'.format(state), index=False)
		#Log out from Fishbowl
		fishpost.logout(cfg['FB']['host'], token)
	except:
	    logging.error(traceback.format_exc())

startExport(cfg['FB']['exportEnabled'].split(","))