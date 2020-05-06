from wtforms import Form, validators, StringField, DecimalField, BooleanField, SelectField
from wtforms.widgets import HiddenInput


class ShopForm(Form):
    # 店铺名称
    shop_name = StringField(
        label="店铺名称:",
        validators=[
            validators.DataRequired(message="店铺名称必须填写!"),
            validators.Length(min=4, max=16, message="店铺名称最短4个字符, 最长16个字符")
        ],
        render_kw={"class": "layui-input lens", "placeholder": "请输入店铺名称"}
    )
    # 是否是品牌
    brand = BooleanField(label="是否品牌:", default=False)
    on_time = BooleanField(label="准时送达:", default=False)
    fengniao = BooleanField(label="蜂鸟速递:", default=False)
    piao = BooleanField(label="是否发票:", default=False)
    bao = BooleanField(label="是否保险:", default=False)
    zhun = BooleanField(label="是否标识:", default=False)

    # 起送价格
    start_send = DecimalField(
        label="起送价格:",
        validators=[
            validators.DataRequired(message="必须填写起送价格")
        ],
        render_kw={"class": "layui-input lens"}
    )
    # 配送费
    send_cost = DecimalField(
        label="配送价格:",
        validators=[
            validators.DataRequired(message="配送费必须填写!")
        ],
        render_kw={"class": "layui-input lens"}
    )
    # 店铺公告
    notice = StringField(
        label="店铺公告:",
        validators=[
            validators.Length(min=10, max=128, message="最短10个字符, 最长128个字符")
        ],
        render_kw={"class": "layui-input lens"}
    )
    # 优惠信息
    discount = StringField(
        label="优惠信息:",
        validators=[
            validators.Length(min=10, max=128, message="最短10个字符, 最长128个字符")
        ],
        render_kw={"class": "layui-input lens"}
    )
    # 店铺图片
    shop_img = StringField(
        label="店铺图片",
        id='image-input',
        widget=HiddenInput()
    )

    # 自定义验证器,验证起送价格和运送费
    def validate_start_send(self, obj):
        obj.data = float('{:.2f}'.format(obj.data))

    def validate_send_cost(self, obj):
        obj.data = float("{:.2f}".format(obj.data))


class MenuCateForm(Form):
    # shop_name = StringField(
    #     label="店铺名称:",
    #     validators=[
    #         validators.DataRequired(message="店铺名称必须填写!"),
    #         validators.Length(min=4, max=16, message="店铺名称最短4个字符, 最长16个字符")
    #     ],
    #     render_kw={"class": "layui-input lens", "placeholder": "请输入店铺名称"}
    # )
    type_accumulation = StringField(
        label="菜品分类:",
        validators=[
            validators.InputRequired(message="菜品分类编号必须填写!"),
            validators.Length(max=32, message="菜品分类最长为16个字符!")
        ],
        render_kw={"class": "layui-input lens"}
    )
    name = StringField(
        label="分类名称:",
        validators=[
            validators.InputRequired(message="菜品分类名称必须填写!"),
            validators.Length(max=32, message="菜品分类 名称最长为32个字符!")
        ],
        render_kw={"class": "layui-input lens"}
    )
    description = StringField(
        label="分类简介:",
        validators=[
            validators.Length(max=128, message="菜品简介最长为128个字符!")
        ],
        render_kw={"class": "layui-input lens"}
    )
    is_default = BooleanField(label="是否默认:", default=False)


class MenusForm(Form):
    goods_name = StringField(
        label="菜品名称:",
        validators=[
            validators.DataRequired(message="菜品名称必须填写!"),
            validators.Length(max=64, message="菜品名称最长64个字符!")
        ],
        render_kw={"class": "layui-input lens"}
    )
    category_id = SelectField(
        label="菜品分类:", coerce=int,
        render_kw={"class": "layui-input lens"}
    )
    goods_price = DecimalField(
        label="菜品价格:", places=2,
        validators=[
            validators.NumberRange(min=0, max=9999, message="菜品价格超出范围"),
            validators.DataRequired(message="菜品价格必须填写!")
        ],
        render_kw={"class": "layui-input lens"}
    )
    tips = StringField(
        label="菜品详情:",
        validators=[
            validators.DataRequired(message="菜品详情必须填写!"),
            validators.Length(max=128, message="菜品详情最长为128个字符!")
        ],
        render_kw={"class": "layui-input lens"}
    )

    # goods_img = StringField(
    #     label="菜品图片:",
    #     id="image-input",
    #     widget=HiddenInput()
    # )

    def validate_goods_price(self, obj):
        obj.data = float("{:.2f}".format(obj.data))

    def __init__(self, shop, *args, **kwargs):
        super(MenusForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [(cate.id, cate.name) for cate in shop.categories]
