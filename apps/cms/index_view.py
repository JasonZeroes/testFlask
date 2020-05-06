from flask import render_template
from flask_login import login_required

from apps.cms import cms_bp


# @cms_bp.route("/", endpoint="首页")
# # @login_required
# def index():
#     if current_user.is_authenticated:
#         # print(current_user.username)
#         return render_template("index.html")
#     else:
#         return redirect(url_for("cms.登录"))


@cms_bp.route("/index/", endpoint="首页")
@login_required
def index():
    return render_template("index.html")
