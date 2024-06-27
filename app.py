#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, jsonify, abort
from jinja2 import Environment, PackageLoader, select_autoescape
from datetime import datetime
import json
import fbdataprocessing.processcsv as fbdata
import os.path, time

# API Key Configuration
api_db = {'dummykey': 'dell'}

app = Flask(__name__)

@app.route('/')
def index():
    return redirect("/WA")

@app.route('/WA')
def pickBySalesWA():
    fbdata.loadDicts("WA")
    lastUpdated = time.ctime(os.path.getmtime('static/dbexport/WAexport.csv'))
    return render_template('template.html', stateName="WA", pickDict=fbdata.filtersoDict('pickitemstatusId',['10','11'],True), commitDict=fbdata.committedDict("30"), backorderDict=fbdata.filterproductDict('pickitemstatusId',['5'],True), totalqty=0, date=datetime.today(), productdict=fbdata.fullProductDict(), lastUpdated=lastUpdated)

@app.route('/QLD')
def pickBySalesQLD():
    fbdata.loadDicts("QLD")
    lastUpdated = time.ctime(os.path.getmtime('static/dbexport/QLDexport.csv'))
    return render_template('template.html', stateName="QLD", pickDict=fbdata.filtersoDict('pickitemstatusId',['10','11','30'],True), commitDict=fbdata.committedDict("40"), backorderDict=fbdata.filterproductDict('pickitemstatusId',['5'],True), totalqty=0, date=datetime.today(), productdict=fbdata.fullProductDict(), lastUpdated=lastUpdated)

@app.route('/SILVER')
def pickBySalesSILVER():
    fbdata.loadDicts("SILVER")
    lastUpdated = time.ctime(os.path.getmtime('static/dbexport/export.csv'))
    return render_template('template.html', stateName="SILVER", pickDict=fbdata.filtersoDict('pickitemstatusId',['10','11'],True), commitDict=fbdata.committedDict(), backorderDict=fbdata.filterproductDict('pickitemstatusId',['5'],True), totalqty=0, date=datetime.today(), productdict=fbdata.fullProductDict(), lastUpdated=lastUpdated)

@app.route('/SP')
def pickBySalesSP():
    fbdata.loadDicts("SP")
    lastUpdated = time.ctime(os.path.getmtime('static/dbexport/export.csv'))
    return render_template('template.html', stateName="SP", pickDict=fbdata.filtersoDict('pickitemstatusId',['10','11'],True), commitDict=fbdata.committedDict(), backorderDict=fbdata.filterproductDict('pickitemstatusId',['5'],True), totalqty=0, date=datetime.today(), productdict=fbdata.fullProductDict(), lastUpdated=lastUpdated)

@app.route('/VIC')
def pickBySalesVIC():
    fbdata.loadDicts("VIC")
    lastUpdated = time.ctime(os.path.getmtime('static/dbexport/export.csv'))
    return render_template('template.html', stateName="VIC", pickDict=fbdata.filtersoDict('pickitemstatusId',['10','11'],True), commitDict=fbdata.committedDict(), backorderDict=fbdata.filterproductDict('pickitemstatusId',['5'],True), totalqty=0, date=datetime.today(), productdict=fbdata.fullProductDict(), lastUpdated=lastUpdated)

@app.route('/delete_row', methods=['GET'])
def delete_row():
    row = request.args.get('row')
    date = request.args.get('dateUntil')
    state = request.args.get('state')
    fbdata.ignoreRow(row,date,state)
    return 'foo'

@app.route('/ignored_orders/<state>')
def ignored_orders(state="WA"):
    return render_template('template_ignored.html', ignoreDict=fbdata.loadIgnoreDict(state))

@app.route('/dell')
def dell():
    lastUpdated = time.ctime(os.path.getmtime(fbdata.latestDellFile()))
    return render_template('template_dell.html', orderDict=fbdata.loadDellPODict(), deliveredDict=fbdata.loadDellDeliveredDict(), lastUpdated=lastUpdated)

@app.route('/dellWebhook', methods=['POST'])
def dellWebhook():
    if request.method == 'POST':
        api_key = request.json.get('api-key')
        if not api_key or not api_db.get(api_key):
            print("Invalid API Key Provided")
            abort(401, 'Invalid API Key')

        # #Authenticated - Start processing data
        data = request.json
        #Testing - just print data directly
        with open("received_data.json", 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return jsonify({'status': 'success', 'data': data}), 200
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006)