#!/usr/bin/python3
"""API Root Module"""

from flask import Flask
from models.storage import storage
from api.v1.views import app_views


if __name__ == "__main__":
    """API Root"""
