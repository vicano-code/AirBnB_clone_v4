#!/usr/bin/python3
"""
Handles RESTFul API actions for Amenity objects view
"""
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenity():
    """retrieves the list of all Amenity objects"""
    amenity_list = [obj.to_dict() for obj in storage.all('Amenity').values()]
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """retrieves an Amenity object given its id"""
    amenity_obj = storage.get('Amenity', amenity_id)
    if amenity_obj is None:
        abort(404)
    return jsonify(amenity_obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """delete an Amenity object"""
    amenity_obj = storage.get('Amenity', amenity_id)
    if amenity_obj is None:
        abort(404)
    storage.delete(amenity_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """creates/post an Amenity object to storage"""
    try:
        data_obj = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data_obj.keys():
        return jsonify({"error": "Missing name"}), 400
    obj = Amenity(**data_obj)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """updates an amenity object"""
    amenity_obj = storage.get('Amenity', amenity_id)
    if amenity_obj is None:
        abort(404)
    try:
        data_obj = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400
    for k, v in data_obj.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amenity_obj, k, v)
    amenity_obj.save()
    return jsonify(amenity_obj.to_dict()), 200
