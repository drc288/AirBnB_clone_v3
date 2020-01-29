#!/usr/bin/python3
""" View for cities """
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State, City


@app_views.route('states/<state_id>/cities',
                 strict_slashes=False, methods=['GET', 'POST'])
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

    if request.method == 'POST':
        if not request.json:
            abort(400, "Not a JSON")
        if "name" not in request.get_json():
            abort(400, "Missing name")

        the_state = storage.get("State", state_id)
        if the_state is None:
            abort(404)
        new_city = City(name=request.json.get('name', ""), state_id=state_id)
        storage.new(new_city)
        new_city.save()
        return make_response(jsonify(new_city.to_dict()), 201)


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

    """ Updates a city """
    if request.method == 'PUT':
        the_city = storage.get('City', city_id)
        if the_city is None:
            abort(404)
        if not request.json:
            abort(400, "Not a JSON")

        for req in request.json:
            if req not in ['id', 'created_at', 'updated_at']:
                setattr(the_city, req, request.json[req])
        storage.save()
        return make_response(jsonify(the_city.to_dict()), 200)

