"""
This module contains functions to validate user inputs.
"""
import sys
from functools import wraps

from flask import jsonify
from werkzeug.exceptions import NotFound

from model import User

USERNAME_MIN_LENGTH = 3  # Minimum length of username
USERNAME_MAX_LENGTH = 25  # This is the maximum length of a username


def validate_username(username):
    """
    Validate the username.
    Returns True if the username is valid, False otherwise.
    """
    if (not username
            or not isinstance(username, str)  # If the username is not a string
            # If the username is less than the minimum length
            or len(username) < USERNAME_MIN_LENGTH
            # If the username is greater than the maximum length
            or len(username) > USERNAME_MAX_LENGTH
            or username.find(' ') != -1  # If the username contains spaces
            or not username.isalpha()  # Check if the username contains only letters
    ):
        return False
    return True


def is_username_in_db(username):
    """
    Check if the username exists in the database.
    Returns UserObject if the username exists, None otherwise.
    """
    if not username:
        return None
    user = User.query.filter_by(username=username).first()
    return user


def user_id_exists_or_404(func):
    @wraps(func)  # preserve the decorated function attributes
    def wrapper(*args, **kwargs):
        try:
            user_id = kwargs['user_id']
            user = User.query.get_or_404(user_id)
            # add the user object to the function arguments
            kwargs.update({'user_obj': user})
            print(f"{kwargs}")
            return func(*args, **kwargs)
        except NotFound:
            print(sys.exc_info())
            return jsonify({'message': 'User not found'}), 404

    return wrapper
