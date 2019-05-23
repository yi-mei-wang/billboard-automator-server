import peewee as pw
import os
from enum import Enum
from playhouse.hybrid import hybrid_property
# from config import AWS_DOMAIN
from models.base_model import BaseModel
from models.order import Order


class Image(BaseModel):
    class Status(Enum):
        UNVERIFIED = 0
        PASSED = 1
        FAILED = 2

    order_id = pw.ForeignKeyField(Order, backref="pictures")
    path = pw.CharField()
    status = pw.IntegerField(default=Status.UNVERIFIED.value)
    
    @hybrid_property
    def pict_url(self):
        # Returns full url of image
        bucket = os.getenv('S3_BUCKET')
        AWS_DOMAIN = f'https://s3.amazonaws.com/{bucket}'
        return f"{AWS_DOMAIN}/{self.path}"

    def pass_mod(self):
        self.status = Status.PASSED.value
    
    def fail_mod(self):
        self.status = Status.FAILED.value