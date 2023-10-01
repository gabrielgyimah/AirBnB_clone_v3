#!/usr/bin/python3
"""API Root Module"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS

if __name__ == "__main__":
    """API Root"""

    app = Flask(__name__)
    cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

    @app_views.app_errorhandler(404)
    def not_found_error(error):
        """Handlers 404 error"""
        err = {"error": "Not found"}
        return jsonify(err)

    app.register_blueprint(app_views)

    host = os.environ.get("HBNB_API_HOST")
    port = os.environ.get("HBNB_API_PORT")

    if host is None:
        host = "0.0.0.0"
    if port is None:
        port = 5000

    app.run(host, port, threaded=True, debug=True)
