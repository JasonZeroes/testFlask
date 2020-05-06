import random
from flask import current_app, jsonify, g
from flask import request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from apps.apis import api_bp
from apps.forms.buyer_form import BuyerRegisterForm, BuyerLoginForm, BuyerAddressForm
from apps.models import BuyerModel, db
from apps.models.buyer_model import BuyerAddress
from apps.tools.token_tools import token_require


@api_bp.route("/sms/", methods=["GET"], endpoint="get_sms")
def get_sms():
    """验证码的发送"""
    tel = request.args.get("tel")
    if tel:
        code = "".join([str(random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])) for _ in range(4)])
        print("send random code is ", code)
        api_redis = current_app.config.get("API_REDIS")
        api_redis.setex(tel, current_app.config.get("SMS_LIFETIME"), code)

        return jsonify({"status": True, "message": "成功发送验证码!"})
    else:
        return jsonify({"status": False, "message": "电话号码无效!"})


@api_bp.route("/register/", methods=["POST"], endpoint="register")
def buyer_register():
    buyer_form = BuyerRegisterForm(request.form)
    if buyer_form.validate():
        buyer = BuyerModel()
        buyer.set_form_attr(buyer_form.data)
        db.session.add(buyer)
        db.session.commit()
        return jsonify({"status": "true", "message": "注册成功!"})
    else:
        return jsonify({
            "status": "false",
            "message": " ".join(["{}:{}".format(k, v[0]) for k, v in buyer_form.errors.items()])
        })


@api_bp.route("/login/", methods=["POST"], endpoint="login")
def buyer_login():
    """用户登录"""
    buyer_form = BuyerLoginForm(request.form)
    if buyer_form.validate():
        buyer = BuyerModel.query.filter_by(username=buyer_form.name.data).first()
        if buyer and buyer.check_password(buyer_form.password.data):
            s = Serializer(current_app.config["SECRET_KEY"], expires_in=current_app.config["TOKEN_EXPIRES"])

            data = s.dumps({"buyer_id": buyer.id})
            resp = jsonify({"status": "true", "message": "登录成功!", "buyer_id": buyer.id, "username": buyer.username})
            resp.set_cookie("token", data.decode("ascii"))
            return resp
        else:
            return jsonify({"status": "false", "message": "用户名或密码出错!"})
    return jsonify({
        "status": "false",
        "message": " ".join(["{}:{}".format(k, v[0]) for k, v in buyer_form.errors.items()])
    })


@api_bp.route("/address/", methods=["POST"], endpoint="add_address")
@token_require
def add_address():
    """添加地址"""
    address_form = BuyerAddressForm(request.form)
    message = "添加成功!"
    if address_form.validate():
        if not address_form.id.data:
            # 添加地址
            address = BuyerAddress()
            address.user = g.current_user
        else:
            # 修改地址
            addresses = g.current_user.addresses
            address = addresses[address_form.id.data - 1]
            message = "更新成功!"
        address.set_form_attr(address_form.data)
        db.session.add(address)
        db.session.commit()
        return jsonify({"status": "true", "message": message})
    return jsonify({"status": "false", "message": "地址操作失败!"})


@api_bp.route("/address/", methods=["GET"], endpoint="address_list")
@token_require
def address_list():
    addresses = g.current_user.addresses
    address_id = request.args.get("id")
    if address_id:
        return jsonify(dict(addresses[int(address_id) - 1]))
    res = [{**dict(address), "id": num + 1} for num, address in enumerate(addresses)]
    return jsonify(res)



