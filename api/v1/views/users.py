#!/usr/bin/python3
"""Users View Module"""

from flask import make_response
from flask import jsonify
from flask import abort
from flask import request

from models import storage
from models.user import User
from api.v1.views import app_views


user_data = [
        "first_name",
        "last_name",
        "email",
        "password"
    ]


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def users():
    """Returns the list of all User objects"""
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users.values()])


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """Returns a single User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def del_user(user_id):
    """Deletes a single User Object from Storage"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return ({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Creates a User object and saves it to Storage"""
    req_data = request.get_json()
    if not req_data:
        abort(400, "Not a JSON")
    if "email" not in req_data:
        return jsonify({"message": "Missing email"}), 400
    if "password" not in req_data:
        return jsonify({"message": "Missing password"}), 400

    user = User(**req_data)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """Updates a User Object"""
    req_data = request.get_json()
    if not request.is_json:
        abort (400, "Not a JSON")
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    for attr in user.to_dict():
        if attr not in ['id', 'email', 'created_at', 'updated_at'] and attr in req_data:
            setattr(user, attr, req_data[attr])
    storage.save()
    return jsonify(user.to_dict()), 200
