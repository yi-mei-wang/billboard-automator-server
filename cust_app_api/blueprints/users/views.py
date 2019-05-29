from flask import Blueprint, jsonify, request
from peewee import IntegrityError
from werkzeug.security import generate_password_hash
import datetime
import jwt
import sys
import uuid

from app import app
from models.user import User

    
users_api_blueprint = Blueprint('users_api', __name__)


@users_api_blueprint.route('/', methods=['GET'])
def index():
    return jsonify({'name': 'hello world'})


@users_api_blueprint.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    breakpoint()
    # Validation:
    # 1. Check if all fields are keyed in
    # 2. Length
    # 3. Password complexity
    # 4. Email validity

    # Handle missing fields
    # if not data["username"]:
    #     return jsonify({'status': 400 , 'message': 'Username is required'})
    # elif not data["email"]:
    #     return jsonify({'status': 400 , 'message': 'Email is required'})
    # elif not data["password"]:
    #     return jsonify({'status': 400 , 'message': 'Password is required'})

    hashed_password = generate_password_hash(
        data['password'], method='sha256', salt_length=8)

    new_user = User(username=data["username"], password=data["password"],
                    email=data["email"], public_id=uuid.uuid4())

    # Give more specific error messages
    try:
        new_user.save()
        token = jwt.encode({'public_id': new_user.public_id, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=30)}, app.config["SECRET_KEY"])

        return jsonify({'auth_token': token.decode('UTF-8'), 'status': 201, 'message': 'User created', 'user': {'id': new_user.public_id, 'username': new_user.username}})

    # When username and email are taken
    except IntegrityError as e:
        if 'username' in str(e):
            return jsonify({'status': 409, 'message': 'Username is taken'})
        elif 'email' in str(e):
            return jsonify({'status': 409, 'message': 'Email is taken'})
