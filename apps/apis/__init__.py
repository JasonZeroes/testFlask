from flask import Blueprint

# 创建蓝图
api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

from . import shop_api
from . import buyer_api
from . import cart_api
from . import order_api