import peewee as pw
from flask_login import UserMixin
from models.base_model import BaseModel
from werkzeug.security import generate_password_hash


class Customer(BaseModel, UserMixin):
    username = pw.CharField(null=False, unique=True)
    email = pw.CharField(null=False, unique=True)
    password = pw.CharField(null=False)

    def hash_password(self, password):
        self.password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)