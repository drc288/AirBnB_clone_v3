#!/usr/bin/python3
"""API RESTFull place"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route('cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def all_places(city_id):
    """
    GET - get all places if the id exists
    POST - create a place if the id exists
    """
    if request.method == 'GET':
        new_list = []
        data_city = storage.get("City", city_id)
        if data_city is None:
            abort(404)
        for cities in data_city.places:
            new_list.append(cities.to_dict())
        return jsonify(new_list)

    if request.method == 'POST':


@app_views.route('/places/<place_id>', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def places_id(place_id):
    """
    GET - get all the places if id exists
    DELETE - delete the place if id exists
    PUT - update data if id exists
    """
    if request.method == 'GET':
