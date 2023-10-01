#!/usr/bin/python3
"""Place View Module"""

from flask import make_response
from flask import jsonify
from flask import abort
from flask import request

from models import storage
from models.place import Place
from api.v1.views import app_views


@app_views.route("/places", methods=["GET"], strict_slashes=False)
def place():
    """Returns the list of all Place objects"""
    places = storage.all(Place)
    return jsonify([place.to_dict() for place in places.values()])


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """Returns a single Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"], strict_slashes=False)
def del_place(place_id):
    """Deletes a single Place Object from Storage"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return ({}), 200


@app_views.route("/places", methods=["POST"], strict_slashes=False)
def create_place():
    """Creates an Place object and saves it to Storage"""
    req_data = request.get_json()
    if not req_data:
        return jsonify({"message": "Not a JSON"}), 400
    elif "name" not in req_data:
        return jsonify({"message": "Missing name"}), 400
    place = Place(name=req_data["name"])
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Updates an Place Object"""
    req_data = request.get_json()
    if not req_data:
        return jsonify({"message": "Not a JSON"}), 400
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    for attr in place.to_dict():
        if attr not in ['id', 'created_at', 'updated_at'] and attr in req_data:
            setattr(place, attr, req_data[attr])
    storage.save()
    return jsonify(place.to_dict()), 200
