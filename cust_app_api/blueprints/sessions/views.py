from flask import Blueprint, jsonify, make_response, request
from werkzeug.security import check_password_hash
import datetime
import jwt

from app import app
from models.user import *

import pysnooper

sessions_api_blueprint = Blueprint('sessions_api', __name__)


@sessions_api_blueprint.route('/login', methods=['POST'])
@pysnooper.snoop('logs.txt')
def login():
    auth = request.get_json()

    if not auth or not auth['username'] or not auth['password']:
        # WWW_Authenticate is a response header
        return make_response('Credentials not provided', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    user = User.get_or_none(username=auth['username'])
    print(user)

    if not user:
        return make_response('User not found', 408, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    # If password is valid
    if check_password_hash(user.password, auth['password']):
        token = user.encode_auth_token()
        return jsonify({'auth_token': token.decode('UTF-8'), 'message': "Successfully signed in", 'status': 201, 'user': {'id': user.id, 'username': user.username}})

    return make_response('Password incorrect', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
