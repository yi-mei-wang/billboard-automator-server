from datetime import datetime
from flask import Blueprint, jsonify, request
from peewee import IntegrityError, fn
from werkzeug.security import generate_password_hash
import sys
import uuid
from models.user import User
from models.order import Order


timeslots_api_blueprint = Blueprint('timeslots_api', __name__)


@timeslots_api_blueprint.route('/show', methods=['GET'])
def show():
    #https://<url>/api/v1/timeslots/show?d=<d>&m=<m>&y=<y>
    d = int(request.args.get('d'))
    m = int(request.args.get('m'))
    y = int(request.args.get('y'))

    # Select all the orders that match the selected_date
    query = Order.select().where((fn.date_trunc('day', Order.start_time) == datetime(y, m, d)))
    slots_taken = [q.start_time for q in query]
    
    return jsonify({'slotsTaken': slots_taken})

