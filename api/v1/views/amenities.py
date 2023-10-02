#!/usr/bin/python3
"""Amenity View Module"""

from flask import make_response
from flask import jsonify
from flask import abort
from flask import request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenity():
    """Returns the list of all Amenity objects"""
    amenities = storage.all(Amenity)
    return jsonify([amenity.to_dict() for amenity in amenities.values()])


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET"], strict_slashes=False)
def get_amenity(amenity_id):
    """Returns a single Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"], strict_slashes=False)
def del_amenity(amenity_id):
    """Deletes a single Amenity Object from Storage"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return ({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Creates an Amenity object and saves it to Storage"""
    req_data = request.get_json()
    if not req_data:
        return make_response(jsonify({"message": "Not a JSON"}), 400)
    elif "name" not in req_data:
        return jsonify({"message": "Missing name"}), 400
    amenity = Amenity(**req_data)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an Amenity Object"""
    req_data = request.get_json()
    if not req_data:
        return jsonify({"message": "Not a JSON"}), 400
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    for attr in amenity.to_dict():
        if attr not in ['id', 'created_at', 'updated_at'] and attr in req_data:
            setattr(amenity, attr, req_data[attr])
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
