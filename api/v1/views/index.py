#!/usr/bin/python3
"""Request Status Module"""

# Standard library imports
from flask import jsonify
from flask import make_response

# Related third-party imports
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {
        "Amenity": Amenity,
        "City": City,
        "Place": Place,
        "Review": Review,
        "State": State,
        "User": User
    }

mods = [
        "amenities",
        "cities",
        "places",
        "reviews",
        "states",
        "users"
]


@app_views.route("/status", strict_slashes=False)
def status():
    """Returns a json Status"""
    status_msg = {'status': 'OK'}
    return jsonify(status_msg)


@app_views.route("/stats", methods=['GET'], strict_slashes=True)
def index():
    """Returns stats on objects"""
    stats = {}
    i = 0
    for cls in classes:
        count = storage.count(classes[cls])
        stats[mods[i]] = count
        i += 1
    return jsonify(stats)
