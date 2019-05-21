from flask import Blueprint, render_template, request
from app import app
from models.image import Image
from cust_app_web.util.helpers.upload import *

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
    return ""
# Do content moderation by calling an API - extract to helper function

# url_path = handle_upload('user_image')



# Assume only one file first
# How to handle multiple uploads?

# If SFW, save to db

# For testing, check time
