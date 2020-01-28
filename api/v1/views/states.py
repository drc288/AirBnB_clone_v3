#!/usr/bin/python3
from flask import jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def view_states():
    """ Retrieves the list of all State objects """
    new_list = []
    states_obj = storage.all("State")
    for data in states_obj.values():
        new_list.append(data.to_dict())

    return jsonify(new_list)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def view_state_id(state_id):
    """ REtrieves the state based on the ID """
    states_obj = storage.all("State")

    for state in states_obj.values():
        if state.id == state_id:
            id_found = state.to_dict()
            return jsonify(id_found)
    abort(404)
