import datetime
from flask import Blueprint, abort, flash, jsonify, redirect, render_template, url_for
from flask_login import current_user, login_required
from peewee import IntegrityError
from cust_app_web.util.helpers.upload import *
from cust_app_web.util.helpers.moderation import *
from models.image import *


orders_blueprint = Blueprint("orders", __name__, template_folder='templates')


@orders_blueprint.route('/')
def index():
    # Display all the orders
    return ""


@orders_blueprint.route('/new', methods=["GET"])
def new():
    # Need to display the available time slots efficiently
    # Check the selected time slot against the db, if conflict -> error
    return render_template('orders/new.html')


@orders_blueprint.route('/create', methods=["POST"])
@login_required
def create():
    ########## TIME SLOT #############
    # Get the current_user
    user = current_user
    # Get the chosen date and time slot
    time_slot = request.form.get('time-slot')
    # Create a new Order entry if time slot if not taken
    try:
        q = Order(user_id=user.id, time_slot=time_slot)
    except IntegrityError:
        # Bad UX if user has to reupload everything, how do I solve this?
        flash('Time slot taken, please choose another one', 'warning')
 
    ############ IMAGE ###############
    # Obtain paths from uploading to AWS
    paths = handle_upload('file')
    urls = full_paths(paths)
    
    # Moderate the content
    errors = moderate(urls)

    # If content is safe for advertising
    if not len(errors):
        for path in paths:
            q = Image(order_id=1, path=path)
            if q.save():
                # Redirect users to payment
                return jsonify({'msg' : 'success'})
                # return redirect(url_for('images.new'))


    # How do I trigger an error response?
    abort(400)
    return jsonify({'msg': 'illegal'})

    # If all goes well, redirect to payment page
    return redirect(url_for('payments.new'))