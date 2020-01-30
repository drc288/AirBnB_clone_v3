#!/usr/bin/python3
"""Create a basics routes and register the blueprint"""
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from os import getenv
from models import storage
from api.v1.views import app_views
app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def tear_down_db(cl):
    """Close the storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Return error page"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(getenv('HBNB_API_PORT', '5000')),
            threaded=True, debug=True)
