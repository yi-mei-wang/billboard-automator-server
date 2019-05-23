import datetime
import peewee as pw
from enum import Enum
from models.base_model import BaseModel
from models.user import User


class Order(BaseModel):
    class Status(Enum):
        UNVERIFIED = 0
        PASSED = 1
        FAILED = 2

    user_id = pw.ForeignKeyField(User, backref="orders", unique=False)
    start_time = pw.DateTimeField(null=False)
    # End time is always start + 15 mins
    end_time = pw.DateTimeField(null=False)
    status = pw.IntegerField(default=Status.UNVERIFIED.value)

    def save(self, *args, **kwargs):
        self.errors = []

        if len(self.errors) == 0:
            self.updated_at = datetime.datetime.now()
            return super(BaseModel, self).save(*args, **kwargs)
        else:
            return 0

    # def end_time(self):
    #     print(self.start_time)
    #     self.end_time = datetime.datetime(self.start_time) + datetime.timedelta(minutes=15)

    def pass_mod(self):
        self.status = Status.PASSED.value
    
    def fail_mod(self):
        self.status = Status.FAILED.value