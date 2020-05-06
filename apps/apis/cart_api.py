import json

from flask import request, jsonify, g, render_template
from flask import current_app
from apps.apis import api_bp
from apps.models import BuyerModel, MenusModel
from apps.tools.token_tools import token_require


def clear_cart(buyer: BuyerModel):
    """清除购物车"""
    api_redis = current_app.config.get("API_REDIS")
    cart_key = f"cart_{buyer.id}"
    res = api_redis.hgetall(cart_key)
    if res:
        # redis中含有该用户的数据
        api_redis.delete(cart_key)


def get_cart(buyer: BuyerModel):
    """获取购物车数据"""
    api_redis = current_app.config.get("API_REDIS")
    cart_key = f"cart_{buyer.id}"
    goods = api_redis.hgetall(cart_key)
    return goods


@api_bp.route("/cart/", methods=["POST"], endpoint="add_cart")
@token_require
def add_cart():
    """添加购物车"""
    good_ids = request.form.getlist("goodsList[]")
    good_nums = request.form.getlist("goodsCount[]")
    api_redis = current_app.config.get("API_REDIS")
    # 判断是否有商品和上平数量
    if len(good_ids) and len(good_nums):
        buyer = g.current_user
        cart_key = f"cart_{buyer.id}"
        clear_cart(buyer)

        # 清空购物车后,重新添加数据
        for good_id, good_num in zip(good_ids, good_nums):
            food = MenusModel.query.filter_by(id=good_id).first()
            food_info = {
                "amount": good_num,
                "goods_name": food.goods_name,
                "goods_price": food.goods_price,
                "goods_img": food.goods_img
            }
            api_redis.hset(cart_key, good_id, json.dumps(food_info))
            api_redis.expire(cart_key, current_app.config.get("CART_LIFETIME", 3600))
        return jsonify({"status": "true", "message": "添加成功!"})
    else:
        return jsonify({"status": "false", "message": "食品数据无效!"})


@api_bp.route("/cart/", methods=["GET"], endpoint="get_cart_goods")
@token_require
def get_cart_goods():
    goods = get_cart(g.current_user)
    total = 0
    res = []
    for good_id, good_info in goods.items():
        good_info = json.loads(good_info)
        good_info["good_id"] = int(good_id)
        total += (good_info.get("goods_price") * int(good_info.get("amount")))
        res.append(good_info)
    return jsonify({"goods_list": res, "totalCost": total})
