import peewee as pw
import os
from clarifai.rest import ClarifaiApp
from enum import Enum
from playhouse.hybrid import hybrid_property
# from config import AWS_DOMAIN
from app import app
from models.base_model import BaseModel
from models.order import Order
import pysnooper


app = ClarifaiApp(api_key=os.getenv('CLARIFAI_API_KEY'))
bucket = os.getenv('S3_BUCKET')
AWS_DOMAIN = f'https://s3.amazonaws.com/{bucket}'


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
        return f"{AWS_DOMAIN}/{self.path}"

    def pass_mod(self):
        self.status = Status.PASSED.value

    def fail_mod(self):
        self.status = Status.FAILED.value

    @pysnooper.snoop('log.txt')
    def moderate(self):
        models = [app.models.get('cigarettes'), app.models.get('moderation')]
        errors = []
        for model in models:
            res = {}
            response = model.predict_by_url(
                url=f"{AWS_DOMAIN}/{self.path}")
            results = response['outputs'][0]['data']['concepts']
            for i, v in enumerate(results):
                if results[i]['value'] > 0.6 and results[i]['name'] not in 'safe':
                    res['error'] = results[i]['name']
                    errors.append(res)

        return errors
