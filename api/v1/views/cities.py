#!/usr/bin/python3
""" View for cities """
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State, City

@app_views.route('states/<state_id>/cities', strict_slashes=False, methods=['GET'])
def view_city(state_id):
    """ Get cities in a State"""
    if request.method == 'GET':
        cities = []
        the_state = storage.get("State", state_id)
        if not the_state:
            abort(404)
        for city in the_state.cities:
            cities.append(city.to_dict())
        return jsonify(cities)
