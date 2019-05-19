from flask import jsonify, make_response, request
from flask_cors import CORS
from werkzeug.security import check_password_hash
import datetime
import jwt

from app import app
from models.user import User

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


## API Routes
from display_api.blueprints.users.views import users_api_blueprint


app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')

@app.route('/login')
def login():
    auth = request.authorization
    print(auth)

    if not auth or not auth.username or not auth.password:
        # WWW_Authenticate is a response header
        return make_response('Could not verify1', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.get(username=auth.username)
    print(user)

    if not user:
        return make_response('Could not verify2', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config["SECRET_KEY"])
        return jsonify({'token': token.decode('UTF-8')})
    
    return make_response('Could not verify3', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})