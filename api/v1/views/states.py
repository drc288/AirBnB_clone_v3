#!/usr/bin/python3
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/states', methods=['GET'])
def view_states():
    """ Retrieves the list of all State objects """
    states_obj = storage.all("State").values().to_dict()
    return states_obj
