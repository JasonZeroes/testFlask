from functools import wraps
from flask import current_app, g
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from flask import request, jsonify

from apps.models import BuyerModel


def token_require(fn):
    """token认证装饰器"""

    @wraps(fn)
    def decorated(*args, **kwargs):
        # 判断cookie中是否含有token信息
        token = request.cookies.get("token")
        if not token:
            return jsonify({"status": "false", "message": "没有token!"})
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired):
            return jsonify({"status": "false", "message": "无效的token"})
        buyer_id = data.get("buyer_id")
        # 判断用户信息
        buyer = BuyerModel.query.filter_by(id=buyer_id).first()
        if not buyer:
            return jsonify({"status": "false", "message": "非法用户!"})
        g.current_user = buyer
        return fn(*args, **kwargs)
    return decorated


