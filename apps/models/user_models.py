from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from apps.models import db
from . import BaseModel


class UserModel(BaseModel, UserMixin):
    """创建用户模型表"""
    username = db.Column(db.String(32), unique=True, nullable=True, index=True)
    _password = db.Column("password", db.String(128), nullable=True)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)

    def check_password(self, user_password):
        return check_password_hash(self._password, user_password)
