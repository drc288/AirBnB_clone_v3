#!/usr/bin/python3
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status():
    """show status page"""
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def stats():
    """  retrieves the number of each objects by type """

    my_dict = {}
    my_dict['amenities'] = storage.count("Amenity")
    my_dict['cities'] = storage.count("City")
    my_dict['places'] = storage.count("Place")
    my_dict['reviews'] = storage.count("Review")
    my_dict['users'] = storage.count("User")
    my_dict['states'] = storage.count("State")

    return jsonify(my_dict)
