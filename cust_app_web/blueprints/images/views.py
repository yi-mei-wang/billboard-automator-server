from flask import Blueprint


images_blueprint = Blueprint("images", __name__, template_folder='templates')


@images_blueprint.route('/')
def index():
    # Display all the images
    return ""


@images_blueprint.route('/new')
