from flask import Blueprint, render_template, request
import datetime


orders_blueprint = Blueprint("orders", __name__, template_folder='templates')


@orders_blueprint.route('/')
def index():
    # Display all the orders
    return ""


@orders_blueprint.route('/new', methods=["GET"])
def new():
    return render_template('orders/new.html')


@orders_blueprint.route('/create', methods=["POST"])
def create():
    data = request.form.get('something')

    # Check the the time from the form against datetime.datetime.now()
    # if within a certain criteria, send to the database, if not, send to socket