#!/usr/bin/python3
"""City View Module"""

from flask import jsonify
from flask import make_response
from flask import abort
from flask import request
from models.state import State
from models import storage
from models.city import City
from api.v1.views import app_views


@app_views.route(
    "/states/<state_id>/cities",
    methods=["GET"],
    strict_slashes=False)
def city(state_id):
    """Returns the list of all City objects"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = storage.all(City)
    res_cities = []
    for city in cities.values():
        if city.state_id == state.id:
            res_cities.append(city)
    return jsonify([city.to_dict() for city in res_cities])


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """Returns a single City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def del_city(city_id):
    """Deletes a single City Object from Storage"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route(
    "/states/<state_id>/cities",
    methods=["POST"],
    strict_slashes=False
    )
def create_city(state_id):
    """Creates an City object and saves it to Storage"""
    req_data = request.get_json()
    if not req_data:
        return make_response(jsonify({"message": "Not a JSON"}), 400)
    elif "name" not in req_data:
        return jsonify({"message": "Missing name"}), 400
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    city = City(name=req_data["name"], state_id=state_id)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """Updates an City Object"""
    req_data = request.get_json()
    if not req_data:
        return jsonify({"message": "Not a JSON"}), 400
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    for attr in city.to_dict():
        if attr not in ['id', 'created_at', 'updated_at'] and attr in req_data:
            setattr(city, attr, req_data[attr])
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)


if __name__ == "__main__":
    main()
