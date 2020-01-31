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
        city = storage.get("City", city_id)
        if city is None:
            abort(404)
        if not request.json:
            abort(400, "Not a JSON")
        if 'user_id' not in request.json:
            abort(400, 'Missing user_id')
        if 'name' not in request.json:
            abort(400, 'Missing name')

        user = storage.get("User", request.get_json()["user_id"])
        if user is None:
            abort(404)
        new_data = request.get_json()
        new_data["city_id"] = city_id
        place = Place(**new_data)
        storage.new(place)
        place.save()
        return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def places_id(place_id):
    """
    GET - get all the places if id exists
    DELETE - delete the place if id exists
    PUT - update data if id exists
    """
    if request.method == 'GET':
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)
        else:
            return jsonify(place.to_dict())

    if request.method == 'DELETE':
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)
        else:
            place.delete()
            storage.save()
            return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        instance = storage.get("Place", place_id)
        if instance is None:
            abort(404)
        else:
            if not request.json:
                abort(400, "Not a JSON")

            my_json = request.get_json()
            for key, value in my_json.items():
                if key not in ['id', 'user_id', 'city_id',
                               'created_at', 'updated_at']:
                    setattr(instance, key, value)
            storage.save()
            return make_response(jsonify(instance.to_dict()), 200)
