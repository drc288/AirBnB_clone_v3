#!/usr/bin/python3
""" View for states """
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def view_states():
    """ Retrieves the list of all State objects """
    if request.method == 'GET':
        new_list = []
        states_obj = storage.all("State")
        for data in states_obj.values():
            new_list.append(data.to_dict())

        return jsonify(new_list)

    if request.method == 'POST':
        if 'name' not in request.get_json():
            abort(400, "Missing name")
        if not request.get_json():
            abort(400, "Not a JSON")
        new_state = State(**request.get_json())
        new_state.save()
        return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def view_state_id(state_id):
    """ REtrieves the state based on the ID """
    states_obj = storage.all("State")
    if request.method == 'GET':
        for state in states_obj.values():
            if state.id == state_id:
                id_found = state.to_dict()
                return jsonify(id_found)
        abort(404)

    if request.method == 'DELETE':
        for state in states_obj.values():
            if state.id == state_id:
                storage.delete(state)
                storage.save()
                return jsonify({}), 200
        abort(404)

    if request.method == 'PUT':
        key = "State." + state_id
        states = storage.all("State")
        instance = states.get(key)
        if instance is None:
            abort(404)
        else:
            if not request.get_json():
                abort(404, "Not a JSON")
            req_var = request.get_json()
            for key, value in req_var.items():
                setattr(instance, key, value)
            storage.save()
            return make_response(jsonify(instance.to_dict()), 200)
