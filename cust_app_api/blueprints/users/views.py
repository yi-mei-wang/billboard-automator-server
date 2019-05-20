from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from peewee import IntegrityError
import sys
import uuid
from models.user import User


users_api_blueprint = Blueprint('users_api', __name__)


@users_api_blueprint.route('/', methods=['GET'])
def index():
    return jsonify({'name': 'hello world'})


@users_api_blueprint.route('/', methods=['POST'])
def create():
    data = request.get_json()

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


    hashed_password = generate_password_hash(data['password'], method='sha256', salt_length=8)

    new_user = User(username=data["username"], password=hashed_password, email=data["email"], public_id=uuid.uuid4())

    # Give more specific error messages
    try:
        new_user.save()
        return jsonify({'status': 201, 'message': 'User created'})

    # When username and email are taken
    except IntegrityError as e:
        if 'username' in str(e):
            return jsonify({'status': 409, 'message': 'Username is taken'})
        elif 'email' in str(e):
            return jsonify({'status': 409, 'message': 'Email is taken'})
    
