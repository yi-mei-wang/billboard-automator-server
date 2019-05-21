from flask import Blueprint, render_template, request
from app import app
from models.image import Image
from cust_app_web.util.helpers.upload import *
from cust_app_web.util.helpers.moderation import *

import pysnooper

images_blueprint = Blueprint("images", __name__, template_folder='templates')


@images_blueprint.route('/')
def index():
    # Display all the images
    return ""


@images_blueprint.route('/new', methods=["GET"])
def new():
    return render_template('images/new.html')


@images_blueprint.route('/create', methods=["POST"])
@pysnooper.snoop('log.txt')
def create():
    # Obtain paths from uploading to AWS
    paths = handle_upload('user_image')
    urls = full_paths(paths)

    # Moderate the content
    for url in urls:
        res = moderate(url)
    # If content is safe for advertising, add to the database
    # Save to the database
        

    # Redirect users to the payment page
    return redirect(url_for('images.new'))
# Do content moderation by calling an API - extract to helper function

# url_path = handle_upload('user_image')



# Assume only one file first
# How to handle multiple uploads?

# If SFW, save to db

# For testing, check time
