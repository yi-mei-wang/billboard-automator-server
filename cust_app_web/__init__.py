from app import app
from cust_app_web.blueprints.images.views import images_blueprint
from flask import render_template
from flask_assets import Environment
from .util.assets import bundles


assets = Environment(app)
assets.register(bundles)


# Register blueprints here
app.register_blueprint(images_blueprint, url_prefix='images')

@app.route('/')
def home():
    return render_template('home.html')

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def access_denied(e):
    return render_template('403.html'), 403


app.register_error_handler(403, access_denied)
app.register_error_handler(404, page_not_found)
app.register_error_handler(500, internal_server_error)