import datetime
from flask import Blueprint, abort, jsonify, request
from peewee import IntegrityError

from cust_app_api.util.helpers.payments import *
from models.image import *
from models.order import *
from models.user import *


payments_api_blueprint = Blueprint("payments_api", __name__)


@payments_blueprint.route('/<recipient>/new', methods=["GET"])
def new(recipient):
    client_token = generate_client_token()
    url = Post.get(Post.path == recipient).post_url
    return render_template('payments/new.html', client_token=client_token, recipient=recipient, url=url)


@payments_blueprint.route('/<recipient>', methods=['POST'])
def create(recipient):
    amount = request.form.get('amount')

    result = make_transaction(amount)

    # If transaction is successful
    if result.is_success or result.transaction:
        post = Post.get(Post.path == recipient)
        recipient_email = User.get(User.id == post.user_id).email
        # Save amount into database
        q = Donation(donor=User.get_by_id(current_user.id),
                     recipient_post=post, amount=amount)
        if q.save():
            # Display on the screen
            # Send an email
            send_email(recipient_email)


    else:
        for x in result.errors.deep_errors:
            return(f'Error: %s: %s' % (x.code, x.message))

