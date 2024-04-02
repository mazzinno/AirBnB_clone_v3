#!/usr/bin/python3
''' Runs the web app '''
import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)


from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {'message': 'This is sample data from the API'}
    return jsonify(data)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
