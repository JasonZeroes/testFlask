from flask import Blueprint

cms_bp = Blueprint("cms", __name__)

from . import index_view
from . import user_view
from . import shop_view
