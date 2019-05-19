from flask import Blueprint, jsonify, request
from models.user import User
from werkzeug.security import generate_password_hash
from peewee import IntegrityError


users_api_blueprint = Blueprint('users_api', __name__)


@users_api_blueprint.route('/', methods=['GET'])
def index():
    return jsonify({'name': 'hello world'})


@users_api_blueprint.route('/', methods=['POST'])
def create():
    data = request.get_json()

    # Validation:
    # 1. Length
    # 2. Password complexity
    # 3. Email validity

    hashed_password = generate_password_hash(data['password'], method='sha256', salt_length=8)

    new_user = User(username=data["username"], password=hashed_password, email=data["email"])

    # Give more specific error messages
    try:
        new_user.save()
        return jsonify({'status': 201, 'message': 'User created'})

    except IntegrityError as e:
        if 'username' in str(e):
            return jsonify({'status': 400, 'message': 'Username is taken'})
        elif 'email' in str(e):
            return jsonify({'status': 400, 'message': 'Email is taken'})
