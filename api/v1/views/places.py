#!/usr/bin/python3
"""
places.py
"""
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from . import app_views


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404, "City not found")
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_by_id(place_id):
    """Retrieves a Place object by its ID"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404, "Place not found")
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place_by_id(place_id):
    """Deletes a Place object by its ID"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404, "Place not found")
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a new Place object"""
    if not request.is_json:
        return make_response("Not a JSON", 400)
    data = request.get_json()
    name = data.get('name')
    user_id = data.get('user_id')

    if not name:
        return make_response("Missing name", 400)
    if not user_id:
        return make_response("Missing user_id", 400)

    user = storage.get(User, user_id)
    if not user:
        abort(404, "User not found")

    new_place = Place(name=name, city_id=city_id, user_id=user_id)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object by its ID"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404, "Place not found")

    if not request.is_json:
        return make_response("Not a JSON", 400)
    data = request.get_json()

    ignored_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
