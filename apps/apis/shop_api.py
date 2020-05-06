from flask import jsonify, request

from apps.apis import api_bp
from apps.models import ShopModel


@api_bp.route("/shop_list/", methods=["GET"], endpoint="商铺列表")
def shop_list():
    shop = ShopModel.query.filter(ShopModel.is_status == 0).all()
    data = [{**dict(x), "id": x.pub_id} for x in shop]
    return jsonify(data)


@api_bp.route("/shop/", methods=["GET"], endpoint="商铺详情")
def shop_detail():
    shop_pid = request.args.get('id')
    shop = ShopModel.query.filter_by(pub_id=shop_pid).first()

    # 查询店铺下的所有分类
    cates = shop.categories
    commodity = [{**dict(cate), "goods_list": [{**dict(x), "goods_id": x.id} for x in cate.menus]} for cate in cates]
    data = {**dict(shop), "id": shop.pub_id, "commodity": commodity, "evaluate": []}
    return jsonify(data)
