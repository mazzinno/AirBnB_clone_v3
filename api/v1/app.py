#!/usr/bin/python3
''' Runs the web app '''
import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    '''
    teardown app context
    '''
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    '''
    teardown app context
    '''
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=os.getenv('HBNB_API_PORT', '5000'), threaded=True)
