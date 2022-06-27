"""
This module contains endpoints for the user Resource
"""
import sys

from flask import jsonify, Blueprint, request
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest, Conflict

from helpers.validation import validate_username, user_id_exists_or_404
from model import User, db

users_bp = Blueprint('users_api', __name__, url_prefix='/users')


@users_bp.route('/')
def get_users():
    """
    Get all users.
    ___

    returns:
    - 200: OK
        A list of users.
    """
    users = User.query.all()
    return jsonify([user.serialize for user in users]), 200


@users_bp.route('/<int:user_id>')
@user_id_exists_or_404
def get_user(user_id, user_obj):
    """
    Get a user by id
    ___

    parameters:
        user_id: The id of the user
    returns:
        - 200: OK
            The user object.
        - 404: Not Found
            message:The user with the given id was not found.
    """
    # Get the user_obj added via the user_id_exists_or_404 decorator
    user = user_obj
    return jsonify(user.serialize), 200


@users_bp.route('/', methods=['POST'])
def create_user():
    """
    Create a user.
    ___

    parameters:
        username: The username of the user.
    returns:
        - 201: Created
            The user object.
        - 400: Bad Request
            message: Invalid request data.
        - 409: Conflict
            message: Username already exists.
    """
    try:
        username = request.json['username']
        if not validate_username(username):
            raise BadRequest
        if User.query.filter_by(username=username).first():
            raise Conflict
        user = User(username=username)
        user.insert()
        db.session.refresh(user)
    except (BadRequest, KeyError):
        print(sys.exc_info())
        db.session.rollback()
        return jsonify({'message': 'Invalid request data'}), 400
    except (IntegrityError, Conflict):
        print(sys.exc_info())
        db.session.rollback()
        return jsonify({'message': f'Username {username} already exists'}), 409
    return jsonify(user.serialize), 201


@users_bp.route('/<int:user_id>', methods=['PUT'])
@user_id_exists_or_404
def update_user(user_id, user_obj):
    """
    Update a user.
    ___

    parameters:
        user_id: The id of the user.
    body:
        username: The username of the user.
    returns:
        - 200: OK
            The user object.
        - 204: No Content
            No new updates were made to the user.
        - 400: Bad Request
            message: Invalid request data.
        - 404: Not Found
            message:The user with the given id was not found.
        - 409: Conflict
            message: Username already exists.
    """
    try:
        # Get the user_obj added via the user_id_exists_or_404 decorator
        user = user_obj
        username = request.json['username']

        if not validate_username(username):
            raise BadRequest
        if user.username == username:
            return '', 204

        username_already_assigned_another_user = User.query.filter(
            User.id.notin_([user_id])).filter(User.username.ilike(username)).first()

        if username_already_assigned_another_user:
            raise Conflict

        user.username = username
        user.update()
    except (BadRequest, KeyError):
        print(sys.exc_info())
        db.session.rollback()
        return jsonify({'message': 'Invalid request data'}), 400
    except (IntegrityError, Conflict):
        print(sys.exc_info())
        db.session.rollback()
        return jsonify({'message': f'Username {username} already exists'}), 409
    return jsonify(user=user.serialize,
                   message="User Updated Successfully"), 200


@users_bp.route('/<int:user_id>', methods=['DELETE'])
@user_id_exists_or_404
def delete_user(user_id, user_obj):
    """
    Delete a user.
    ___

    parameters:
        user_id: The id of the user.
    returns:
        - 200: OK
            The user object.
        - 404: Not Found
            message:The user with the given id was not found.
    """
    # Get the user_obj added via the user_id_exists_or_404 decorator
    user = user_obj
    user.delete()
    return jsonify(message=f"User with id {user_id} deleted"), 200
