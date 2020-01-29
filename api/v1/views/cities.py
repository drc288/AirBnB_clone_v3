#!/usr/bin/python3
""" View for cities """
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State, City

