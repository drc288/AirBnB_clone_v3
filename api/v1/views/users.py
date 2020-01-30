#!/usr/bin/python3
""" View for users """
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State, City
from models.user import User


@app_views.route('/users',
                 strict_slashes=False, methods=['GET', 'POST'])
def all_users():
    """ Retrieves a list of all users """
    if request.method == 'GET':
        all_users = []
        users = storage.all("User")
        for user in users.values():
            all_users.append(user.to_dict())

        return jsonify(all_users)

    """ Creates a new User """
    if request.method == 'POST':
        if not request.json:
            abort(400, "Not a JSON")
        if 'email' not in request.json:
            abort(400, "Missing email")
        if 'password' not in request.json:
            abort(400, 'Missing password')

        new_user = User(**request.get_json())
        new_user.save()
        return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>',
                 strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def retrieve_user(user_id):
    """ Retrieves an User """

    if request.method == 'GET':
        the_user = storage.get('User', user_id)
        if the_user is None:
            abort(404)
        return jsonify(the_user.to_dict())

    """ Deletes an USER """
    if request.method == 'DELETE':
        the_user = storage.get("User", user_id)
        if the_user is None:
            abort(404)
        the_user.delete()
        storage.save()
        return make_response(jsonify({}), 200)

    """ Modifies an USER """
    if request.method == 'PUT':
        the_user = storage.get("User", user_id)
        if the_user is None:
            abort(404)

        if not request.json:
            abort(400, 'Not a JSON')

        req_var = request.get_json()
        for key, value in req_var.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(the_user, key, value)

        storage.save()
        return make_response(jsonify(the_user.to_dict()), 200)
