#!/usr/bin/python3
"""
Handles all default RESTFul API actions for Review class
"""
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """retrieves the list of all Review objects of a Place"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    reviews_list = [obj.to_dict() for obj in place.reviews]
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review_by_id(review_id):
    """retrieves a Review object given its id"""
    review_obj = storage.get('Review', review_id)
    if review_obj is None:
        abort(404)
    return jsonify(review_obj.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """delete a Review object"""
    review_obj = storage.get('Review', review_id)
    if review_obj is None:
        abort(404)
    storage.delete(review_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """creates a Review object to storage"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    try:
        data_obj = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in data_obj.keys():
        return jsonify({"error": "Missing user_id"}), 400
    if "text" not in data_obj.keys():
        return jsonify({"error": "Missing text"}), 400

    user = storage.get('User', data_obj['user_id'])
    if user is None:
        abort(404)

    data_obj['place_id'] = place.id
    obj = Review(**data_obj)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """updates a Review object"""
    review_obj = storage.get('Review', review_id)
    if review_obj is None:
        abort(404)
    try:
        data_obj = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400
    for k, v in data_obj.items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review_obj, k, v)
    review_obj.save()
    return jsonify(review_obj.to_dict()), 200
