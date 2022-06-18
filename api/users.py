from flask import jsonify, Blueprint
from model import User


users_bp = Blueprint('users_api', __name__, url_prefix='/users')


@users_bp.route('/')
def get_users():
    users = User.query.all()
    return jsonify([user.serialize for user in users]), 200
