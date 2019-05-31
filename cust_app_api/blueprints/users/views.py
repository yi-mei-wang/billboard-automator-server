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

    hashed_password = generate_password_hash(
        data['password'], method='sha256', salt_length=8)

    new_user = User(username=data["username"], password=hashed_password,
                    email=data["email"], public_id=uuid.uuid4())

    # Give more specific error messages
    try:
        new_user.save()
        token = new_user.encode_auth_token()

        return jsonify({'auth_token': token.decode('UTF-8'), 'status': 201, 'message': 'User created', 'user': {'id': str(new_user.id), 'username': new_user.username}})

    # When username and email are taken
    except IntegrityError as e:
        if 'username' in str(e):
            return jsonify({'status': 4091, 'message': 'Username is taken'})
        elif 'email' in str(e):
            return jsonify({'status': 4092, 'message': 'Email is taken'})
