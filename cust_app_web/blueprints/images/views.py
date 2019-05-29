from flask import Blueprint, abort, jsonify, render_template, request
from app import app
from models.image import Image
from cust_app_web.util.helpers.upload import *
from cust_app_web.util.helpers.moderation import *

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

    errors = {}

    # If content is safe for advertising
    for i, path in enumerate(paths):
        img = Image(order_id=1, path=path)
        # Do the moderation
        errs = img.moderate()
        if not errs:
            # pass -> modify and save
            if img.save():
                # ??
                return jsonify({'msg': 'success'})
        # fail append error along with
        errors[i] = errs
    print(errors)
    return jsonify({'msg': 'illegal', 'errors': errors})
