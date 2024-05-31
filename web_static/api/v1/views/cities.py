#!/usr/bin/python3
"""
Handles RESTFul API actions for City objects view
"""
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_state_cities(state_id):
    """retrieves the list of all City objects of a state"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    city_list = [city.to_dict() for city in state.cities]
    return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id):
    """retrieves a City object given its id"""
    city_obj = storage.get('City', city_id)
    if city_obj is None:
        abort(404)
    return jsonify(city_obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """delete as City object"""
    city_obj = storage.get('City', city_id)
    if city_obj is None:
        abort(404)
    storage.delete(city_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """creates/post a City object to storage"""
    try:
        data_obj = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data_obj.keys():
        return jsonify({"error": "Missing name"}), 400
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    data_obj['state_id'] = state.id
    obj = City(**data_obj)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """updates a City object"""
    city_obj = storage.get('City', city_id)
    if city_obj is None:
        abort(404)
    try:
        data_obj = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400
    for k, v in data_obj.items():
        if k not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city_obj, k, v)
    city_obj.save()
    return jsonify(city_obj.to_dict()), 200
