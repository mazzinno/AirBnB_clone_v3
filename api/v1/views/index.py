#!/usr/bin/python3
""" Main route """
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status')
def status_check():
    '''
    checks status of JSON
    '''
    return jsonify({"status": "OK"})
