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


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending of the JSON in the body
    of the request
    """

    if request.get_json() is None:
        abort(400, description="Not a JSON")

    data = request.get_json()

    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)

    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)

    list_places = []
    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]

    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    return jsonify(places)
