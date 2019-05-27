from datetime import datetime
from flask import Blueprint, jsonify, request
from peewee import IntegrityError, fn
from werkzeug.security import generate_password_hash
import sys
import uuid
from models.image import Image
from models.order import Order
from models.user import User


timeslots_api_blueprint = Blueprint('timeslots_api', __name__)


@timeslots_api_blueprint.route('/show', methods=['GET'])
def show():
    # https://<url>/api/v1/timeslots/show?d=<d>&m=<m>&y=<y>
    d = int(request.args.get('d'))
    m = int(request.args.get('m'))
    y = int(request.args.get('y'))

    slots_taken = []
    # Select all the orders that match the selected_date and has 12 images in the order
    orders = Order.select()\
        .join(Image)\
        .where((fn.date_trunc('day', Order.start_time) == datetime(y, m, d)))\
        .group_by(Order.id)\
        .having(fn.count(Image.id) == 12)

    slots_taken = [o.start_time for o in orders]

    return jsonify({'slotsTaken': slots_taken})
