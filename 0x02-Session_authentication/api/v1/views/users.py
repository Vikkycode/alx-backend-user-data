#!/usr/bin/env python3
"""
Module with all user routes
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users), 200


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ Retrieves a User object """
    if user_id == "me":
        if request.current_user is None:
            abort(404)
        else:
            return jsonify(request.current_user.to_json()), 200

    user = User.get(user_id)
    if user is None:
        abort(404)

    return jsonify(user.to_json()), 200


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = User.get(user_id)

    if user is None:
        abort(404)
    user.remove()

    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User"""
    rj = request.get_json()
    if rj is None:
        abort(400, description="Not a JSON")

    if 'email' not in rj:
        abort(400, description="Missing email")

    if 'password' not in rj:
        abort(400, description="Missing password")

    user = User(**rj)
    user.save()

    return jsonify(user.to_json()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    user = User.get(user_id)

    if user is None:
        abort(404)

    rj = request.get_json()
    if rj is None:
        abort(400, description="Not a JSON")

    for key, value in rj.items():
        if key != "id" and key != "email" and key != "created_at" and\
           key != "updated_at":
            setattr(user, key, value)

    user.save()
    return jsonify(user.to_json()), 200
