#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, jsonify
import fbdataprocessing.processcsv as fbdata
import os, time

# API Key Configuration
api_db = {'dummykey': 'dell'}

app = Flask(__name__)
app.json.sort_keys = False


@app.route('/')
def index():
    return redirect("/api/dashboard/WA")

@app.route('/api/delete_row', methods=['GET'])
def api_delete_row():
    row = request.args.get('row')
    date = request.args.get('dateUntil')
    state = request.args.get('state')
    fbdata.ignoreRow(row,date,state)
    return 'foo'

@app.route('/api/ignored_orders/<state>')
def api_ignored_orders(state="WA"):
    ignoreDict = fbdata.loadIgnoreDict(state)
    return jsonify({
        "ignoreDict": ignoreDict
    })

@app.route('/dell')
def dell():
    lastUpdated = time.ctime(os.path.getmtime(fbdata.latestDellFile()))
    return render_template('template_dell.html', orderDict=fbdata.loadDellPODict(), deliveredDict=fbdata.loadDellDeliveredDict(), lastUpdated=lastUpdated)

@app.route('/api/dashboard/<state>')
def api_dashboard(state):
    print(state)
    fbdata.loadDicts(state)
    print(os.path.dirname('static'))
    return jsonify({
        "pickDict": fbdata.filtersoDict('pickitemstatusId', ['10','11'], True),
        "commitDict": fbdata.committedDict("30"),
        "backorderDict": fbdata.filterproductDict('pickitemstatusId', ['5'], True),
        "lastUpdated": time.ctime(os.path.getmtime('static/dbexport/WAexport.csv'))
    })

###Use the below for testing only - do NOT run this as a production server###
#if __name__ == '__main__':
#    app.run("0.0.0.0", 5006)