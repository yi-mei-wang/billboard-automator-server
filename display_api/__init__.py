from flask_cors import CORS
from app import app

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


## API Routes
from display_api.blueprints.users.views import users_api_blueprint
from display_api.blueprints.sessions.views import sessions_api_blueprint


app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')
app.register_blueprint(sessionss_api_blueprint, url_prefix='/api/v1')
