from os import abort

from flask_login import current_user

from apps.models import ShopModel


def check_shop_pid(pub_id):
    data = ShopModel.query.filter(ShopModel.pub_id == pub_id, ShopModel.seller_id == current_user.id).first()
    return data or abort(404)
