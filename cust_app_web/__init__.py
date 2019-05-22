from app import app
from cust_app_web.blueprints.images.views import images_blueprint
from cust_app_web.blueprints.orders.views import orders_blueprint
from flask import jsonify, render_template
from flask_assets import Environment
from .util.assets import bundles


assets = Environment(app)
assets.register(bundles)


# Register blueprints here
app.register_blueprint(images_blueprint, url_prefix='/images')
app.register_blueprint(orders_blueprint, url_prefix='/orders')


@app.route('/')
def home():
    return render_template('home.html')


@app.errorhandler(400)
def bad_request(e):
    response = jsonify({'code': 400, 'message': 'Image did not pass moderation test'})
    response.status_code = 400
    return response

@app.errorhandler(403)
def access_denied(e):
    return render_template('403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500



app.register_error_handler(400, bad_request)
app.register_error_handler(403, access_denied)
app.register_error_handler(404, page_not_found)
app.register_error_handler(500, internal_server_error)