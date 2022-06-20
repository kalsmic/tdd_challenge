"""
This module contains endpoints for the user Resource
"""
import sys

import sqlalchemy
from flask import jsonify, Blueprint, request
from helpers.validation import validate_username
from werkzeug.exceptions import NotFound, BadRequest, Conflict
from model import User, db
from sqlalchemy.exc import IntegrityError


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
def get_user(user_id):
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
    try:
        user = User.query.get_or_404(user_id)
    except NotFound:
        return jsonify({'message': 'User not found'}), 404
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
