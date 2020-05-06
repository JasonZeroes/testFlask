from apps.models import UserModel
from . import BaseModel, db


class ShopModel(BaseModel):
    """商铺模型"""
    # 店铺外部id
    pub_id = db.Column(db.String(16), unique=True, index=True)
    # 店铺名称
    shop_name = db.Column(db.String(16), nullable=True, unique=True)
    # 店铺评分
    shop_rating = db.Column(db.Float, default=5.0)
    # 是否是品牌
    brand = db.Column(db.Boolean, default=False)
    # 是否准时送达
    on_time = db.Column(db.Boolean, default=True)
    # 是否是蜂鸟配送
    fengniao = db.Column(db.Boolean, default=True)
    # 是否是保险
    bao = db.Column(db.Boolean, default=True)
    # 是否有发票
    piao = db.Column(db.Boolean, default=True)
    # 是否准标识
    zhun = db.Column(db.Boolean, default=True)
    # 起送价格
    start_send = db.Column(db.Float, default=0)
    # 配送费
    send_cost = db.Column(db.Float, default=0)
    # 店铺图片
    shop_img = db.Column(db.String(128))
    # 店铺公告
    notice = db.Column(db.String(128), default='')
    # 优惠信息
    discount = db.Column(db.String(128), default='')
    # 店铺和商家的关系
    seller_id = db.Column(db.Integer, db.ForeignKey("user_model.id"))
    # 建立连接关系(反向查询)
    seller = db.relationship(UserModel, backref="shops")

    def keys(self):
        return ("shop_name", "shop_rating",
                "brand", "on_time", "fengniao",
                "bao", "piao", "zhun",
                "start_send", "send_cost", "shop_img",
                "notice", "discount")


class MenuCateModel(BaseModel):
    """菜品分类"""
    # 分类编号
    type_accumulation = db.Column(db.String(16))
    # 分类名称
    name = db.Column(db.String(32))
    # 分类描述
    description = db.Column(db.String(128), default='')
    # 是否设为默认
    is_default = db.Column(db.Boolean, default=False)
    # 归属店铺
    shop_pid = db.Column(db.String(32), db.ForeignKey("shop_model.pub_id"))
    # 与店铺建立连接关系
    shop = db.relationship(ShopModel, backref="categories")

    def keys(self):
        return "type_accumulation", "name", "description", "is_default"


class MenusModel(BaseModel):
    # 菜品名称
    goods_name = db.Column(db.String(64))
    # 菜品评分
    rating = db.Column(db.Float, default=5.0)
    # 归属店铺
    shop_id = db.Column(db.String(16), db.ForeignKey("shop_model.pub_id"))
    # 归属分类
    category_id = db.Column(db.Integer, db.ForeignKey("menu_cate_model.id"))
    # 和菜品表建立连接关系
    cate = db.relationship(MenuCateModel, backref="menus")
    # 菜品价格
    goods_price = db.Column(db.Float, default=0.0)
    # 月销售额
    month_sales = db.Column(db.Integer, default=0)
    # 评分数量
    rating_count = db.Column(db.Integer, default=0)
    # 菜品提示信息
    tips = db.Column(db.String(128), default="")
    # 菜品图片
    goods_img = db.Column(db.String(128), default="")

    def keys(self):
        return "goods_name", "rating", "goods_price", "tips", "goods_img"
