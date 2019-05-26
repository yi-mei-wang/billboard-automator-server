import datetime
from flask import Blueprint, abort, jsonify, request
from peewee import IntegrityError
from cust_app_web.util.helpers.upload import *
from cust_app_web.util.helpers.moderation import *
from models.image import *
from models.order import *


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

    # Create a new Order entry if time slot if not taken
    try:
        order = Order(user_id=20, start_time=chosen_date)
        order.save()
    except IntegrityError:
        # Bad UX if user has to reupload everything, how do I solve this?
        print('Time slot taken, please choose another one', 'warning')

    # ############ IMAGE ###############
    # Obtain paths from uploading to AWS
    paths = handle_upload('file')
    urls = full_paths(paths)

    # Moderate the content
    # errors = moderate(urls)
    errors = []
    # If content is safe for advertising
    if not len(errors):
        for path in paths:
            q = Image(order_id=order, path=path)
            q.save()
    # Redirect users to payment
    return jsonify({'msg': 'success'})
    # return redirect(url_for('images.new'))

    # How do I trigger an error response?
    abort(400)
    return jsonify({'msg': 'illegal'})
