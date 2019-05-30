import datetime
from flask import Blueprint, abort, jsonify, request
from peewee import IntegrityError
from util.helpers.upload import *
from util.helpers.moderation import *
from models.image import *
from models.order import *
from models.user import *

import pysnooper


orders_api_blueprint = Blueprint("orders_api", __name__)


@orders_api_blueprint.route('/')
def index():
    # Display all the orders
    # When given a user id, fetch all the orders related to that user
    return "hkfds"


@orders_api_blueprint.route('/show')
@pysnooper.snoop('log.txt')
def show():
    # Before or after (-1 is before, 1 is after)
    before_or_after = request.args.get('q')
    # When given a user id, fetch all the orders related to that user

    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return jsonify({'status': '400', 'errors': 'No Auth Header'})

    auth_token = auth_header.split(" ")[1]
    id = User.decode_auth_token(auth_token)

    user = User.get_by_id(id)

    # Get all the orders belonging to the user (> means future, < means past)
    orders = "liren"
    if before_or_after == "1":
        orders = Order.select().where(Order.user_id == user.id,
                                      Order.start_time > datetime.datetime.now(), Order.status == 1)
    elif before_or_after == "-1":
        orders = Order.select().where(Order.user_id == user.id,
                                      Order.start_time < datetime.datetime.now(), Order.status == 1)

    response = []
    for order in orders:
        # Get all the images from each order
        imgs = Image.select().join(Order).where(
            Image.status == 1, Order.id == order.id)

        images = []
        for img in imgs:
            img_url = img.pict_url
            images.append(img_url)

        data = {'order_id': order.id, 'images': images,
                'start_time': order.start_time}
        response.append(data)

    return jsonify(response)


@orders_api_blueprint.route('/create', methods=["POST"])
def create():
    ########## TIME SLOT #############
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
        # If there are no rejects
        if not errs:
            # pass -> save
            img.pass_mod()
            if not img.save():
                print('cry')
        # If there are errors, append error to main json
        errors[i] = errs

    return jsonify({'status': 'ok', 'errors': errors, "order_id": order.id})


@orders_api_blueprint.route('/verify', methods=["POST"])
def verify():
    # Verify that all the images passed the moderation
    data = request.get_json()
    order_id = data['order_id']
    order = Order.get_by_id(int(order_id))
    order.pass_mod()
    return jsonify({'status': 'ok'})
