#!/usr/bin/python3
"""View to handle API actions related to State objects
"""

from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def states_get(state_id=None):
    """Handle State object CRUD operations
    """
    if request.method == 'GET':
        # Get all State objects or a specific one if state_id provided
        if not state_id:
            return jsonify([state.to_dict() for state in storage.all(State).values()]), 200
        state = storage.get(State, state_id)
        return jsonify(state.to_dict()) if state else jsonify(error="Not found"), 404

    elif request.method == 'DELETE':
        # Delete a State object if exists
        state = storage.get(State, state_id)
        if state:
            storage.delete(state)
            storage.save()
            return jsonify({}), 200
        return jsonify(error="Not found"), 404

    elif request.method == 'POST':
        # Create a new State object
        if not request.is_json:
            return jsonify(error="Not a JSON"), 400
        data = request.get_json()
        if 'name' not in data:
            return jsonify(error="Missing name"), 400
        new_state = State(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201

    elif request.method == 'PUT':
        # Update a State object if exists
        state = storage.get(State, state_id)
        if state:
            if not request.is_json:
                return jsonify(error="Not a JSON"), 400
            data = request.get_json()
            for key, value in data.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(state, key, value)
            state.save()
            return jsonify(state.to_dict()), 200
        return jsonify(error="Not found"), 404
