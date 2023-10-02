#!/usr/bin/python3
"""API Root Module"""

import os
from flask import Flask
from flask import jsonify
from flask import make_response
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app_views.app_errorhandler(404)
def not_found_error(error):
    """Handlers 404 error"""
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def end_session(exception=None):
    """Ends the session"""
    storage.close()


app.register_blueprint(app_views)


if __name__ == "__main__":
    host = os.environ.get("HBNB_API_HOST", '0.0.0.0')
    port = os.environ.get("HBNB_API_PORT", 5000)

    app.run(host=host, port=port, threaded=True, debug=True)
