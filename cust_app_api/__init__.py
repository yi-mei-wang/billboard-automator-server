from flask_cors import CORS
from app import app
from cust_app_api.blueprints.images.views import images_api_blueprint
from cust_app_api.blueprints.orders.views import orders_api_blueprint
from cust_app_api.blueprints.sessions.views import sessions_api_blueprint
from cust_app_api.blueprints.timeslots.views import timeslots_api_blueprint
from cust_app_api.blueprints.users.views import users_api_blueprint

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


app.register_blueprint(images_api_blueprint, url_prefix='/api/v1/images')
app.register_blueprint(orders_api_blueprint, url_prefix='/api/v1/orders')
app.register_blueprint(sessions_api_blueprint, url_prefix='/api/v1')
app.register_blueprint(timeslots_api_blueprint, url_prefix='/api/v1/timeslots')
app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')
