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
        cities = storage.all("City")
        if not request.json:
            abort(400, "Not a JSON")
        searching = "City.{}".format(city_id)
        if searching not in cities:
            abort(404)
        if 'user_id' not in request.json:
            abort(400, 'Missing user_id')
        if 'name' not in request.json:
            abort(400, 'Missing name')

        user = storage.get("User", request.get_json()["user_id"])
        if user is None:
            abort(404)
        else:
            place = Place(**request.get_json())
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
            storage.delete(place)
            storage.save()
            return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        places = storage.all("Place")
        instance = places.get("Place.{}".format(place_id))
        if instance is None:
            abort(404)
        else:
            if not request.json:
                abort(400, "Not a JSON")

            my_json = request.get_json()
            for key, value in my_json.items():
                setattr(instance, key, value)
            storage.save()
            return make_response(ify(instance.to_dict()), 200)
