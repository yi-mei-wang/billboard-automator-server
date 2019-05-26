from datetime import datetime
from flask import Blueprint, jsonify, make_response, request
from werkzeug.security import check_password_hash
from models.image import Image
from models.order import Order
from models.user import User

images_api_blueprint = Blueprint('images_api', __name__)


@images_api_blueprint.route('/', methods=['GET'])
def get_current_images():
    # Get the time from the query
    data = request.get_json()
    query_time = datetime.utcfromtimestamp(int(data['utcTime'])/1000)
    # Reset minute to the previous 15 min block
    query_min = query_time.minute
    start_min = query_min - (query_min % 15)
    start_time = query_time.replace(minute=start_min, second=0, microsecond=0)
    # Only choose those that passed the moderation AND belongs to the orders scheduled at start_time
    images = Image.select().join(Order).where(
        Image.status == 1, Order.start_time == start_time)
    output = []
    for img in images:
        image_data = {}
        image_data['order_id'] = str(img.order_id)
        image_data['path'] = img.path
        image_data['status'] = img.status
        image_data['pict_url'] = img.pict_url
        output.append(image_data)

    return jsonify({'images': output})


# @images_api_blueprint.route('/<order_id>', methods=['GET'])
# def get_current_image(order_id):
#     # Maybe it should be user_id have to check
#     image = Image.get_by_id(order_id)

#     if not image:
#         return jsonify({'message': 'No image found'})

#     image_data = {}
#     image_data['order_id'] = img.order_id
#     image_data['path'] = img.path
#     image_data['status'] = img.status
#     image_data['pict_url'] = img.pict_url
#     image_data['pass_mod'] = img.pass_mod
#     image_data['fail_mod'] = img.fail_mod

#     return jsonify({'image': image_data})


# @images_api_blueprint.route('/upload/<order_id>', methods=['POST'])
# def create_image(order_id):
#     data = request.get_json()

#     new_image = Image(pict_url=data['pict_url'])
#     db.session.add(new_image)
#     db.session.commit()

#     return jsonify({'message': 'Image created'})


# @images_api_blueprint.route('/upload/<order_id>', methods=['POST'])
# # Maybe in the address route parameters also put a new_picture_url
# def update_image(order_id, new_picture_url):
#     # Maybe it should be user_id have to check
#     image = Image.select().where(order_id=order_id).first()

#     if not image:
#         return jsonify({'message': 'No image found'})

#     image.pict_url = new_picture_url
#     db.session.commit()

#     return jsonify({'message': 'The image has been updated'})


# @images_api_blueprint.route('/delete/<order_id>', methods=['POST'])
# def delete_image(order_id):
#     # Maybe it should be user_id have to check
#     image = Image.select().where(order_id=order_id).first()

#     if not image:
#         return jsonify({'message': 'No image found'})

#     db.session.delete(image)
#     db.session.commit()

#     return jsonify({'message': 'The user has been deleted'})
