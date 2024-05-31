#!/usr/bin/python3
"""
Handles RESTFul API actions for Place objects view
"""
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """retrieves the list of all Place objects of a City"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    places_list = [obj.to_dict() for obj in city.places]
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_by_id(place_id):
    """retrieves a Place object given its id"""
    place_obj = storage.get('Place', place_id)
    if place_obj is None:
        abort(404)
    return jsonify(place_obj.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """delete a Place object"""
    place_obj = storage.get('Place', place_id)
    if place_obj is None:
        abort(404)
    storage.delete(place_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """creates a Place object to storage"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    try:
        data_obj = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in data_obj.keys():
        return jsonify({"error": "Missing user_id"}), 400
    if "name" not in data_obj.keys():
        return jsonify({"error": "Missing name"}), 400

    user = storage.get('User', data_obj['user_id'])
    if user is None:
        abort(404)

    data_obj['city_id'] = city.id
    obj = Place(**data_obj)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """updates a Place object"""
    place_obj = storage.get('Place', place_id)
    if place_obj is None:
        abort(404)
    try:
        data_obj = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400
    for k, v in data_obj.items():
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place_obj, k, v)
    place_obj.save()
    return jsonify(place_obj.to_dict()), 200
