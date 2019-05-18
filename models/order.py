import peewee as pw

from models.base_model import BaseModel

class Order(BaseModel):
    customer_id = pw.ForeignKeyField(Customer, backref="orders")
    time_slot = pw.DateTimeField(null=False)

    # Return all the orders with time_slot
    # SELECT FROM order WHERE time_slot == xxx