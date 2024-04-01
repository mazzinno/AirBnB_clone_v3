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

@app_views.route('/stats', strict_slashes=False)
def stats():
    """Retrieve count of objects in storage for various classes
    """
    # Import necessary models
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User

    # Define classes and their corresponding names
    classes = {"amenities": Amenity, "cities": City,
               "places": Place, "reviews": Review,
               "states": State, "users": User}
    json_dict = {}

    for name, cls in classes.items():
        json_dict.update({name: storage.count(cls)})

    return jsonify(json_dict)