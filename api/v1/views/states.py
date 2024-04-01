#!/usr/bin/python3
from flask import Flask, jsonify, request, abort
from models import State

app = Flask(__name__)


@app.route('/api/v1/states', methods=['GET'])
def get_states():
    states = State.query.all()
    return jsonify([state.to_dict() for state in states])


@app.route('/api/v1/states/<state_id>', methods=['GET'])
def get_state(state_id):
    state = State.query.get(state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app.route('/api/v1/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    state = State.query.get(state_id)
    if not state:
        abort(404)
    state.delete()
    return jsonify({}), 200


@app.route('/api/v1/states', methods=['POST'])
def create_state():
    if not request.json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    state = State(name=request.json['name'])
    state.save()
    return jsonify(state.to_dict()), 201


@app.route('/api/v1/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    state = State.query.get(state_id)
    if not state:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    for key, value in request.json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
