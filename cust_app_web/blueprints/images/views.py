from flask import Blueprint, render_template, request


images_blueprint = Blueprint("images", __name__, template_folder='templates')


@images_blueprint.route('/')
def index():
    # Display all the images
    return ""


@images_blueprint.route('/new', methods=["GET"])
def new():
    return render_template('images/new.html')


@images_blueprint.route('/create', methods=["POST"])
def create():
    # Do content moderation by calling an API - extract to helper function

    # Assume only one file first

    # If SFW, save to db

    # For testing, check time

    # If time is now, attempt to emit to socket

    # Else no