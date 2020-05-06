from datetime import datetime
import json
import random
import time

from flask import g, request, jsonify

from apps.apis import api_bp
from apps.apis.cart_api import get_cart, clear_cart
from apps.models import OrderModel, MenusModel, OrderGoodsModel, db, ShopModel
from apps.models.buyer_model import BuyerAddress, BuyerModel
from apps.tools.token_tools import token_require


def create_order_sn(uid):
    return "{time_str}{uid}{ran_str}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                             uid=uid,
                                             ran_str=random.randint(10, 99))


def create_order(address: BuyerAddress, user: BuyerModel):
    order = OrderModel(user_id=user.id)

    order.order_code = create_order_sn(user.id)
    order.order_address = str(address)
    print(str(address))
    order.created_time = datetime.now()

    goods = get_cart(g.current_user)
    total = 0
    for good_id, good_info in goods.items():
        good_id = int(good_id)
        good_info = json.loads(good_info)
        food = MenusModel.query.filter_by(id=good_id).first()
        order.shop_pid = food.shop_id
        order.goods.append(
            OrderGoodsModel(goods_id=good_id, goods_name=food.goods_name,
                            goods_img=food.goods_img, goods_price=food.goods_price,
                            amount=int(good_info.get("amount")))
        )
        total += (food.goods_price * int(good_info.get("amount")))
    order.order_price = total
    db.session.add(order)
    db.session.commit()
    return order


@api_bp.route("/order/", methods=["POST"], endpoint="add_order")
@token_require
def add_order():
    user = g.current_user
    address_index = request.form.get("address_id")
    address = user.addresses[int(address_index) - 1]

    order = create_order(address, user)
    clear_cart(user)
    return jsonify({
        "status": "true",
        "message": "添加成功!",
        "order_id": order.order_code
    })


@api_bp.route("/order/", methods=["GET"], endpoint="get_order")
@token_require
def get_order():
    order_sn = request.args.get("id")
    order = OrderModel.query.filter_by(order_code=order_sn).first()
    if order:
        x = [dict(x) for x in order.goods]
        shop = ShopModel.query.filter_by(pub_id=order.shop_pid).first()
        data = {
            **dict(order),
            "id": order.id,
            "order_status": order.get_status(),
            "goods_list": x,
            "order_birth_time": order.created_time.strftime("%Y-%m-%d %H:%M:%S"),
            "shop_img": shop.shop_img
        }
        return jsonify(data)


@api_bp.route("/orders/", methods=["GET"], endpoint="get_orders")
@token_require
def get_orders():
    user = g.current_user
    data = [{
        "id": order.order_code,
        "order_birth_time": order.created_time.strftime("%Y-%m-%d %H:%M"),
        **dict(order),
        "shop_name": order.shop.shop_name,
        "shop_img": order.shop.shop_img,
        "goods_list": [dict(x) for x in order.goods],
        "order_status": order.get_status(),
    } for order in user.orders]
    return jsonify(data)
