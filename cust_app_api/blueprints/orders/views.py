import datetime
from flask import Blueprint, abort, jsonify
from peewee import IntegrityError
from cust_app_web.util.helpers.upload import *
from cust_app_web.util.helpers.moderation import *
from models.image import *


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
    data = request.get_json()

    # Create a new Order entry if time slot if not taken
    try:
        q = Order(user_id=20, start_time=data['timeSlot'])
        q.save()
    except IntegrityError:
        # Bad UX if user has to reupload everything, how do I solve this?
        print('Time slot taken, please choose another one', 'warning')
    
    return jsonify({'msg': 'ok'})
    # ############ IMAGE ###############
    # # Obtain paths from uploading to AWS
    # paths = handle_upload('file')
    # urls = full_paths(paths)
    
    # # Moderate the content
    # errors = moderate(urls)

    # # If content is safe for advertising
    # if not len(errors):
    #     for path in paths:
    #         q = Image(order_id=1, path=path)
    #         if q.save():
    #             # Redirect users to payment
    #             return jsonify({'msg' : 'success'})
    #             # return redirect(url_for('images.new'))


    # # How do I trigger an error response?
    # abort(400)
    # return jsonify({'msg': 'illegal'})

    # # If all goes well, redirect to payment page
    # return redirect(url_for('payments.new'))