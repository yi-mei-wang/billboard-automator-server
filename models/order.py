import peewee as pw
from models.base_model import BaseModel
from models.user import User


class Order(BaseModel):
    user_id = pw.ForeignKeyField(User, backref="orders")
    time_slot = pw.DateTimeField(null=False)

    # Return all the orders with time_slot
    # SELECT FROM order WHERE time_slot == xxx