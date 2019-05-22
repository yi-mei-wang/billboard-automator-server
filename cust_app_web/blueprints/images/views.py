from flask import Blueprint, jsonify, render_template, request
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
def create():
    # Obtain paths from uploading to AWS
    paths = handle_upload('file')
    urls = full_paths(paths)
    

    # Moderate the content
    errors = moderate(urls)
    print(errors)

    # If content is safe for advertising
    if not len(errors):
        for path in paths:
            q = Image(order_id=1329, path=path)
            if q.save():
                # Redirect users to payment
                return jsonify({'msg' : 'success'})
                # return redirect(url_for('images.new'))


    # Redirect users back to images.new
    # return redirect(url_for('images.new'))
    return jsonify({'msg': 'illegal'})