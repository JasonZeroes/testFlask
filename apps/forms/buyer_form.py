from wtforms import Form, StringField, validators, PasswordField, IntegerField
from flask import current_app

from apps.models.buyer_model import BuyerModel


class BuyerLoginForm(Form):
    name = StringField(
        validators=[
            validators.DataRequired(message="请输入用户名信息!"),
            validators.Length(max=32, message="用户名最长不能超过32个字符!")
        ]
    )
    password = PasswordField(
        validators=[
            validators.DataRequired(message="用户密码必须填写!"),
            validators.Length(max=16, message="密码不能超过16个字符!")
        ]
    )


class BuyerRegisterForm(Form):
    username = StringField(
        validators=[
            validators.DataRequired(message="用户名必须填写!"),
            validators.Length(max=32, message="用户名不能超过32个字符!")
        ],
    )
    password = PasswordField(
        validators=[
            validators.DataRequired(message="密码必须填写!"),
            validators.Length(max=16, message="密码最长为16个字符!")
        ],
    )
    tel = StringField(
        validators=[
            validators.DataRequired(message="电弧号码必须填写!"),
            validators.Regexp(r'^(13[0-9])|(14[5-7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9]|166|168|199)\d{8}$',
                              message="请输入正确的电话号码!")
        ],
    )

    # 验证码
    sms = StringField(validators=[validators.DataRequired(message="请输入验证码!")])

    # 验证用户名是否重名
    def validate_username(self, value):
        u = BuyerModel.query.filter_by(username=value.data).first()
        if u:
            raise validators.ValidationError("该用户名已经被注册了!")

    # 验证手机号码
    def validate_tel(self, value):
        u = BuyerModel.query.filter_by(tel=value.data).first()
        if u:
            raise validators.ValidationError("该手机号码已经被注册了!")

    # 验证验证码
    def validate_sms(self, value):
        api_redis = current_app.config.get("API_REDIS")
        raw_code = api_redis.get(self.tel.data).decode("ascii")
        if not raw_code:
            raise validators.ValidationError("验证码失效!请点击重新获取验证码!")
        if raw_code != value.data:
            raise validators.ValidationError("验证码错误!")


class BuyerAddressForm(Form):
    id = IntegerField(default=0)
    provence = StringField(
        validators=[
            validators.DataRequired(message="省份信息必须填写!"),
            validators.Length(max=8, message="最长为8个字符!")
        ],
    )
    city = StringField(
        validators=[
            validators.DataRequired(message="城市信息必须填写!"),
            validators.Length(max=16, message="最长为16个字符!")
        ],
    )
    area = StringField(
        validators=[
            validators.DataRequired(message="县区必须填写!"),
            validators.Length(max=16, message="最长16个字符!")
        ],
    )
    detail_address = StringField(
        validators=[
            validators.DataRequired("详细信息必须填写!"),
            validators.Length(max=64, message="最长为64个字符!")
        ],
    )
    name = StringField(
        validators=[
            validators.DataRequired("收货人姓名必须填写!"),
            validators.Length(max=32, message="最长为32个字符!")
        ],
    )
    # 收货人电话
    tel = StringField(
        validators=[
            validators.DataRequired(message="收货人电话必须填写!"),
            validators.Regexp(r'^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18['
                              r'0-9])|166|198|199)\d{8}$', message="请输入正确的电话号码")
        ],
    )
