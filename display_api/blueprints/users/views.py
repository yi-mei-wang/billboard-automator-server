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

    hashed_password = generate_password_hash(data['password'], method='sha256', salt_length=8)

    new_user = User(username=data["username"], password=hashed_password, email=data["email"])

    # Give more specific error messages
    try:
        new_user.save()
        return jsonify({'message': 'User has been created'})

    except IntegrityError as e:
        print(f"heelo {e}")
        return jsonify({'message': 'An error occurred'})