#!/usr/bin/python3
from flask import Flask, make_response, jsonify
from os import getenv
from models import storage
from api.v1.views import app_views
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down_db(cl):
    """Close the storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Return error page"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(os.getenv('HBNB_API_PORT', '5000')),
            threaded=True, debug=True)
