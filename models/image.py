import peewee as pw
import os
from playhouse.hybrid import hybrid_property
# from config import AWS_DOMAIN
from models.base_model import BaseModel
from models.order import Order


class Image(BaseModel):
    order_id = pw.ForeignKeyField(Order, backref="pictures")
    path = pw.CharField()
    status = pw.IntegerField(default=0)
    
    @hybrid_property
    def pict_url(self):
        AWS_DOMAIN = os.getenv('AWS_DOMAIN')
        return f"{AWS_DOMAIN}/{self.path}"
