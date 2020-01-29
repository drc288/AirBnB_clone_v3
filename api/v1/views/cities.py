#!/usr/bin/python3
""" View for cities """
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State, City


@app_views.route('states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def view_city(state_id):
    """ Get cities in a State"""
    if request.method == 'GET':
        cities = []
        the_state = storage.get('State', state_id)
        if not the_state:
            abort(404)
        for city in the_state.cities:
            cities.append(city.to_dict())
        return jsonify(cities)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET', 'DELETE'])
def view_city_id(city_id):
    """ gets a city """

    if request.method == 'GET':
        the_city = storage.get("City", city_id)
        if the_city is None:
            abort(404)
        return jsonify(the_city.to_dict())

    """ Deletes a city based on the ID """
    if request.method == 'DELETE':
        the_city = storage.get("City", city_id)
        if the_city is None:
            abort(404)
        the_city.delete()
        storage.save()
        return make_response(jsonify({}), 200)
