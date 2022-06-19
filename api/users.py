from flask import jsonify, Blueprint
from werkzeug.exceptions import NotFound
from model import User



users_bp = Blueprint('users_api', __name__, url_prefix='/users')


@users_bp.route('/')
def get_users():
    """
    Get all users.
    Returns:
    - 200: OK
        A list of users.
    """
    users = User.query.all()
    return jsonify([user.serialize for user in users]), 200


@users_bp.route('/<int:user_id>')
def get_user(user_id):
    """
    Get a user by id
    
    :param user_id: The id of the user
    :return: 
        - 200: OK
            The user object.
        - 404: Not Found
            Message:The user with the given id was not found.
    """
    try:
        user = User.query.get_or_404(user_id)
    except NotFound:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user.serialize), 200