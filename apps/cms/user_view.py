from flask import request, render_template, redirect, url_for, session
from flask_login import login_user, logout_user, login_required

from apps.cms import cms_bp
from apps.forms.user_forms import RegisterForm, LoginForm
from apps.models import UserModel, db


@cms_bp.route("/register/", methods=["GET", "POST"], endpoint="注册")
def register():
    """实现用户注册"""
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        # 将数据保存到数据库当中
        username = form.username.data
        user = db.session.query(UserModel).filter_by(username=username).first()
        if user is None:
            # 将用户提交的数据保存到数据库
            user = UserModel()
            user.set_form_attr(form.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("cms.登录"))
        form.username.errors.append("用户名已注册!")

    return render_template("reg-log.html", form=form, flags="注册")


@cms_bp.route("/login/", methods=["GET", "POST"], endpoint="登录")
def login():
    """实现用户登录"""
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        # 到数据库查验用户的合法性
        username = form.username.data
        user = db.session.query(UserModel).filter_by(username=username).first()
        if user and user.check_password(form.password.data):
            # 设置session
            login_user(user)
            referer = request.args.get("next")
            return redirect(referer or url_for("cms.首页"))
        form.username.errors.append("用户名或者密码错误!")
    return render_template("reg-log.html", form=form, flags="登录")


@cms_bp.route("/logout/", methods=["GET", "POST"], endpoint="退出")
def logout():
    logout_user()
    return redirect(url_for("cms.登录"))


# @cms_bp.route("/a/")
# @login_required
# def aa():
#     return "哈哈哈!"
