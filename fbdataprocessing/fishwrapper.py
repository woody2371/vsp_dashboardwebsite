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

cfg = configparser.ConfigParser()
cfg.read('config.ini')

logging.basicConfig(filename=cfg['SYSTEM']['writepath']+'FBAPI.log',level=logging.DEBUG,format='%(asctime)s %(message)s')

wa_query = """
SELECT so.num, soitem.productNum, so.billToName, pickitem.qty, qtyinventory.qtyonhand - qtycommitted.qty as qtyonhand, qtyinventory.qtyonorderpo, qtyinventory.qtyonorderto, (qtyinventory.qtyonorderpo + qtyinventory.qtyonorderto) as qtyonordertotal,soitem.statusId as soitemstatusId, so.statusId as sostatusId, pickitem.statusId as pickitemstatusId, soitem.typeId as soitemtypeId, soitem.dateLastModified, soitem.note, so.salesman, pick.locationgroupid
FROM soitem
LEFT JOIN so
    ON so.id = soitem.soid
LEFT JOIN pickitem
    ON pickitem.soItemId = soitem.id
LEFT JOIN part
            ON part.defaultProductId = soitem.productid
LEFT JOIN (SELECT * FROM qtyinventory WHERE locationgroupid = "7") as qtyinventory
        ON qtyinventory.partid = part.id
LEFT JOIN (SELECT * FROM qtycommitted WHERE locationgroupid = "7") as qtycommitted
                ON qtycommitted.partid = part.id
LEFT JOIN (SELECT * FROM pick WHERE locationgroupid = "7") as pick
                ON pickitem.pickId = pick.id
WHERE pick.locationgroupId = "7"
AND (soitem.statusId LIKE "10" OR soitem.statusId LIKE "30" OR soitem.statusId LIKE "20")
AND (so.statusId LIKE "20" OR so.statusId LIKE "25")
AND productNum NOT LIKE ("NX-%") AND productNum NOT LIKE ("FREIGHT%") AND productNum NOT LIKE ("HIK-CENTRAL-P%")
AND soitem.typeId NOT LIKE ("90")
"""

# global functions
def xmlparse(xml):
	""" global function for parsing xml """
	root = etree.fromstring(xml)
	return root

if(cfg['FB']['WAexportEnabled'] == "yes"):
	print("Starting Data Import")
	try:
		#Log into Fishbowl and return auth token
		print("Logging in")
		token = fishpost.login(cfg['FB']['host'], cfg['FB']['appName'], cfg['FB']['appDescription'], cfg['FB']['appId'], cfg['FB']['username'], cfg['FB']['password'])
		#Download data - SQL query can be modified in config file
		print("Logged in, downloading data")
		dataReturn = fishpost.dataQuery(cfg['FB']['host'], token, wa_query)
		print("Data downloaded, logging out")
		#Log out from Fishbowl
		fishpost.logout(cfg['FB']['host'], token)

        #Move data to a pandas dataframe
		df = pd.json_normalize(json.loads(dataReturn.text))
		
		#Write data to CSV
		df.to_csv(cfg['SYSTEM']['XMLwritepath']+'WAexport.csv', index=False)

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

