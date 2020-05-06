from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    is_status = db.Column(db.SmallInteger, default=0)

    def set_form_attr(self, form_data: dict):
        for k, v in form_data.items():
            if hasattr(self, k) and k != "id":
                setattr(self, k, v)

    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item)


from .user_models import UserModel
from .shop_models import ShopModel
from .shop_models import MenuCateModel
from .shop_models import MenusModel
from .buyer_model import BuyerModel
from .order_models import OrderModel, OrderGoodsModel
