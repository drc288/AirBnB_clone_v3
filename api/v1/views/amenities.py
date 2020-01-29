#!/usr/bin/python3
"""APISET amenities"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def all_amenities():
    """
    Get - get all amenities reprs obj
    Post - create a new obj
    """
    if request.method == 'GET':
        new_list = []
        for amenity in storage.all("Amenity").values():
            new_list.append(amenity.to_dict())

        return jsonify(new_list)

    if request.method == 'POST':
        if not request.json:
            abort(400, "Not a JSON")
        if 'name' not in request.get_json():
            abort(400, "Missing name")
        amenity = Amenity(**request.get_json())
        amenity.save()
        return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def view_amenity_id(amenity_id):
    """
    GET - get the datat if the id exists
    DELETE - delete data if the id exists
    PUT - Update the data if the id exists
    """
    if request.method == 'GET':
        amenity = storage.get("Amenity", amenity_id)
        if amenity is None:
            abort(404)
        else:
            return jsonify(amenity.to_dict())

    if request.method == 'DELETE':
        amenity = storage.get("Amenity", amenity_id)
        if amenity is None:
            abort(404)
        else:
            storage.delete(amenity)
            storage.save()
            return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        amenities = storage.all("Amenity")
        instance = amenities.get("Amenity.{}".format(amenity_id))
        if instance is None:
            abort(404)
        else:
            if not request.json:
                abort(400, "Not a JSON")

            my_json = request.get_json()
            for key, value in my_json.items():
                setattr(instance, key, value)
            storage.save()
            return make_response(jsonify(instance.to_dict()), 200)
