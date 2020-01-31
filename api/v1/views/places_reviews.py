#!/usr/bin/python3
"""API RESTFull reviews"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route('places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def all_reviews(place_id):
    """
    GET - get all reviews
    POST - create new review
    """
    if request.method == 'GET':
        new_list = []
        data_place = storage.get("Place", place_id)
        if data_place is None:
            abort(404)
        for state in data_place.reviews:
            new_list.append(state.to_dict())
        return jsonify(new_list)

    if request.method == 'POST':
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)
        if not request.json:
            abort(400, "Not a JSON")
        if "user_id" not in request.json:
            abort(400, "Missing user_id")
        if "text" not in request.json:
            abor(400, "Missing text")

        user = storage.get("User", request.get_json()["user_id"])
        if user is None:
            abort(404)
        new_data = request.get_json()
        new_data["place_id"] = place_id
        review = Review(**new_data)
        storage.new(review)
        review.save()
        return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def review_id(review_id):
    """
    GET - get all review if the id exists
    DELETE - delete the revew if id exists
    PUT - update the data if the id exists
    """
    if request.method == 'GET':
        review = storage.get("Review", review_id)
        if review is None:
            abort(404)
        else:
            return jsonify(review.to_dict())

    if request.method == 'DELETE':
        review = storage.get("Review", review_id)
        if review is None:
            abort(404)
        else:
            review.delete()
            storage.save()
            return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        instance = storage.get("Review", review_id)
        if instance is None:
            abort(404)
        else:
            if not request.josn:
                abort(400, "Not a JSON")

            my_json = request.get_json()
            for key, value in my_json.items():
                if key not in ['id', 'user_id', 'place_id',
                               'created_at', 'updated_at']:
                    setattr(instance, key, value)
            storage.save()
            return make_response(jsonify(instance.to_dict()), 200)
