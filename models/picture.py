import peewee as pw
from playhouse.hybrid import hybrid_property
from config import AWS_DOMAIN
from models.base_model import BaseModel


class Picture(BaseModel):
    order_id = pw.ForeignKeyField(Order, backref="pictures")
    path = pw.CharField()
    
    @hybrid_property
    def pict_url(self):
        return f"{AWS_DOMAIN}/{self.path}"
