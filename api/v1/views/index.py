#!/usr/bin/python3
""" Main route """
from models import storage
from flask import jsonify
from api.v1.views import app_views
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {
           "amenities": Amenity,
           "cities": City,
           "places": Place,
           "reviews": Review,
           "states": State,
           "users": User,
           }


@app_views.route('/status')
def status_check():
    '''
    checks status of JSON
    '''
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def retrieve_number():
    '''
    retrieves number of objects by type
    '''
    obj_dict = {}
    for key, value in classes.items():
        obj_dict[key] = storage.count(value)
    return jsonify(obj_dict)
