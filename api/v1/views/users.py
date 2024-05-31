#!/usr/bin/python3
"""
Handles RESTFul API actions for User objects view
"""
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """retrieves the list of all User objects"""
    user_list = [obj.to_dict() for obj in storage.all('User').values()]
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user_by_id(user_id):
    """retrieves a User object given its id"""
    user_obj = storage.get('User', user_id)
    if user_obj is None:
        abort(404)
    return jsonify(user_obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """delete a User object"""
    user_obj = storage.get('User', user_id)
    if user_obj is None:
        abort(404)
    storage.delete(user_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """creates a User object to storage"""
    try:
        data_obj = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400
    if "email" not in data_obj.keys():
        return jsonify({"error": "Missing email"}), 400
    if "password" not in data_obj.keys():
        return jsonify({"error": "Missing password"}), 400
    obj = User(**data_obj)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """updates a User object"""
    user_obj = storage.get('User', user_id)
    if user_obj is None:
        abort(404)
    try:
        data_obj = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400
    for k, v in data_obj.items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user_obj, k, v)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 200
