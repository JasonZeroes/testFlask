from apps.models import BaseModel, db, BuyerModel, ShopModel


class OrderModel(BaseModel):
    """订单表"""
    # 订单编号
    order_code = db.Column(db.String(32), unique=True)
    shop_pid = db.Column(db.String(16), db.ForeignKey("shop_model.pub_id"))
    # 买家id信息
    user_id = db.Column(db.Integer, db.ForeignKey("buyer_model.id"))
    # 送货地址
    order_address = db.Column(db.String(128))
    # 订单金额
    order_price = db.Column(db.Float, default=0)
    # 订单状态
    order_status = db.Column(db.Integer, default=0)
    # 订单产生时间
    created_time = db.Column(db.DateTime, onupdate=True)
    # 第三方交易号
    trade_sn = db.Column(db.String(128), default="")
    user = db.relationship("BuyerModel", backref="orders")
    shop = db.relationship("ShopModel", backref="orders")

    def keys(self):
        return "order_address", "order_code", "order_price"

    def get_status(self):
        if self.order_status == 0:
            return "待付款"
        else:
            return "已付款"


class OrderGoodsModel(BaseModel):
    """订单商品表"""
    # 订单id号
    order_id = db.Column(db.Integer, db.ForeignKey("order_model.id"))
    # 商品id号
    goods_id = db.Column(db.Integer)
    # 商品名称
    goods_name = db.Column(db.String(64))
    # 上平图片
    goods_img = db.Column(db.String(128), default="")
    # 商品价格
    goods_price = db.Column(db.Float)
    # 商品的数量
    amount = db.Column(db.Integer)
    order = db.relationship(OrderModel, backref="goods")

    def keys(self):
        return "goods_id", "amount", "goods_name", "goods_img", "goods_price"
