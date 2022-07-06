#!/usr/bin/python
# -*- coding: utf-8 -*-
import struct
import datetime
import base64
import configparser
import logging
import traceback
from lxml import etree

import pandas as pd
from statuscodes import getstatus
import fishpost

cfg = configparser.ConfigParser()
cfg.read('/home/tom/Projects/vsp_dashboardwebsite/config.ini')

logging.basicConfig(filename=cfg['SYSTEM']['writepath']+'FBAPI.log',level=logging.DEBUG,format='%(asctime)s %(message)s')

# global functions
def xmlparse(xml):
	""" global function for parsing xml """
	root = etree.fromstring(xml)
	return root

if(cfg['FB']['WAexportEnabled'] == "yes"):
	
	#Log into Fishbowl and return auth token
	token = fishpost.login(cfg['FB']['host'], cfg['FB']['appName'], cfg['FB']['appDescription'], cfg['FB']['appId'], cfg['FB']['username'], cfg['FB']['password'])
	#Download data - SQL query can be modified in config file
	dataReturn = fishpost.dataQuery(cfg['FB']['host'], token, cfg['SQL']['WA'])
	#Log out from Fishbowl
	fishpost.logout(cfg['FB']['host'], token)

	try: 
		#Convert response to JSON, then normalize using Panda's library
		json_data = pd.json_normalize(dataReturn.json())

		#Use Panda's to_csv function to write the new export
		json_data.to_csv(cfg['SYSTEM']['XMLwritepath']+'WAExport.csv', index=False)

	except:
		logging.error(traceback.format_exc())

# if(cfg['FB']['QLDexportEnabled'] == "yes"):
#     stream = Fishbowlapi(cfg['FB']['user'], cfg['FB']['passwd'], cfg['FB']['host'])
#     dataReturn = stream.execute_query(cfg['FB']['QLDexportName'])
#     try:
#         stream.logout()
#         stream.close()
#     except:
#             pass
#     with open(cfg['SYSTEM']['XMLwritepath']+'QLDexport.csv', 'w', newline='') as exportFile:
#             try:
#                     if xmlparse(dataReturn)[1][0][0].tag == "Rows":
#                             for line in xmlparse(dataReturn)[1][0][0]:
#                                     exportFile.write(line.text + "\r\n")
#                     else:
#                             logging.error("QLD Data export failed, instead of Rows dataReturn showed " + xmlparse(dataReturn)[1][0][0].tag)
#             except:
#                     logging.error(traceback.format_exc())


#     try:
#             #Only enable below for passing data via FTP back to base
#             #fishbowlFTP.placeFile(cfg['SYSTEM']['writepath']+'QLDexport.csv','QLDexport.csv')
#             pass
#     except:
#             logging.error(traceback.format_exc())

# if(cfg['FB']['NSWexportEnabled'] == "yes"):
#     stream = Fishbowlapi(cfg['FB']['user'], cfg['FB']['passwd'], cfg['FB']['host'])
#     dataReturn = stream.execute_query(cfg['FB']['NSWexportName'])
#     stream.logout()
#     stream.close()

#     with open(cfg['SYSTEM']['XMLwritepath']+'NSWexport.csv', 'w', newline='') as exportFile:
#             try:
#                     if xmlparse(dataReturn)[1][0][0].tag == "Rows":
#                             for line in xmlparse(dataReturn)[1][0][0]:
#                                     exportFile.write(line.text + "\r\n")
#                     else:
#                             logging.error("NSW Data export failed, instead of Rows dataReturn showed " + xmlparse(dataReturn)[1][0][0].tag)
#             except:
#                     logging.error(traceback.format_exc())


#     try:
#             #Only enable below for passing data via FTP back to base
#             #fishbowlFTP.placeFile(cfg['SYSTEM']['writepath']+'NSWexport.csv','NSWexport.csv')
#             pass
#     except:
#             logging.error(traceback.format_exc())

# if(cfg['FB']['SAexportEnabled'] == "yes"):
#     stream = Fishbowlapi(cfg['FB']['user'], cfg['FB']['passwd'], cfg['FB']['host'])
#     dataReturn = stream.execute_query(cfg['FB']['SAexportName'])
#     stream.logout()
#     stream.close()

#     with open(cfg['SYSTEM']['XMLwritepath']+'SAexport.csv', 'w', newline='') as exportFile:
#             try:
#                     if xmlparse(dataReturn)[1][0][0].tag == "Rows":
#                             for line in xmlparse(dataReturn)[1][0][0]:
#                                     exportFile.write(line.text + "\r\n")
#                     else:
#                             logging.error("SA Data export failed, instead of Rows dataReturn showed " + xmlparse(dataReturn)[1][0][0].tag)
#             except:
#                     logging.error(traceback.format_exc())


#     try:
#             #Only enable below for passing data via FTP back to base
#             #fishbowlFTP.placeFile(cfg['SYSTEM']['writepath']+'SAexport.csv','SAexport.csv')
#             pass
#     except:
#             logging.error(traceback.format_exc())

# if(cfg['FB']['VICexportEnabled'] == "yes"):
#     stream = Fishbowlapi(cfg['FB']['user'], cfg['FB']['passwd'], cfg['FB']['host'])
#     dataReturn = stream.execute_query(cfg['FB']['VICexportName'])
#     stream.logout()
#     stream.close()

#     with open(cfg['SYSTEM']['XMLwritepath']+'VICexport.csv', 'w', newline='') as exportFile:
#             try:
#                     if xmlparse(dataReturn)[1][0][0].tag == "Rows":
#                             for line in xmlparse(dataReturn)[1][0][0]:
#                                     exportFile.write(line.text + "\r\n")
#                     else:
#                             logging.error("VIC Data export failed, instead of Rows dataReturn showed " + xmlparse(dataReturn)[1][0][0].tag)
#             except:
#                     logging.error(traceback.format_exc())


#     try:
#             #Only enable below for passing data via FTP back to base
#             #fishbowlFTP.placeFile(cfg['SYSTEM']['writepath']+'VICexport.csv','VICexport.csv')
#             pass
#     except:
#             logging.error(traceback.format_exc())

