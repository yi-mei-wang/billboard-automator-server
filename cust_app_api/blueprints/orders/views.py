import datetime
from flask import Blueprint, abort, jsonify, request
from peewee import IntegrityError
from cust_app_web.util.helpers.upload import *
from cust_app_web.util.helpers.moderation import *
from models.image import *
from models.order import *
from models.user import *


orders_api_blueprint = Blueprint("orders_api", __name__)


@orders_api_blueprint.route('/')
def index():
    # Display all the orders
    return "hkfds"


@orders_api_blueprint.route('/create', methods=["POST"])
def create():
    ########## TIME SLOT #############
    # Get the current_user
    # user = current_user
    # Get the chosen date and time slot
    files = request.files.getlist('file')
    chosen_date = datetime.datetime.utcfromtimestamp(
        int(request.form.get('chosenDate'))/1000)
    auth_token = request.form.get('auth_token')
    user_id = User.decode_auth_token(auth_token)
    user = User.get_by_id(user_id)
    # Create a new Order entry if time slot if not taken
    try:
        order = Order(user_id=user_id, start_time=chosen_date)
        order.save()
    except IntegrityError:
        # Bad UX if user has to reupload everything, how do I solve this?
        print('Time slot taken, please choose another one', 'warning')

    # ############ IMAGE ###############
    # Obtain paths from uploading to AWS
    paths = handle_upload('file')
    urls = full_paths(paths)
    errors = {}

    # If content is safe for advertising
    for i, path in enumerate(paths):
        img = Image(order_id=order.id, path=path)
        # Do the moderation
        errs = img.moderate()
        # If there are no errors
        if not errs:
            # pass -> save
            if not img.save():
                print('cry')
        # If there are errors, append error to main json
        errors[i] = errs
    print(errors)
    return jsonify({'status': 'ok', 'errors': errors})
