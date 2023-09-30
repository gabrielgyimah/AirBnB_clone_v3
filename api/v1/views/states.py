#!/usr/bin/python3
"""View Module for State"""

from models import storage
from api.v1.views import app_views
from models.state import State
from flask import jsonify
from flask import abort
from flask import request
from models.base_model import BaseModel


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def states():
    """Retrieves the list of all State objects"""
    db_states = storage.all(State)
    return jsonify([state.to_dict() for state in db_states.values()])

@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def state(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route("/states/<state_id>", methods=['DELETE'], strict_slashes=False)
def delete(state_id):
    """Deletes a state object from storage"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

@app_views.route("/states", methods=['POST'], strict_slashes=False)
def create():
    """Creates a new state object and saves it to storage"""
    req_data = request.get_json()
    if not req_data:
        return jsonify({"message": "Not a JSON"}), 400
    elif not req_data["name"]:
        return jsonify({"message": "Missing name"}), 400
    state = State(name=req_data['name'])
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update(state_id):
    """Updates a State Object in the Storage"""
    req_data = request.get_json()
    if not req_data:
        return jsonify({"message": "Not a JSON"}), 400
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    for attr in state.to_dict():
        if attr not in ['id', 'created_at', 'updated_at'] and attr in req_data:
            setattr(state, attr, req_data[attr])
    storage.save()
    return jsonify(state.to_dict()), 200


if __name__ == "__main__":
    main()
