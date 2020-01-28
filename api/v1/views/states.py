#!/usr/bin/python3
from flask import jsonify
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
