import uuid
from flask import render_template, request, url_for, redirect, session, jsonify
from flask_login import login_required, current_user
from qiniu import Auth, put_data

from apps.cms import cms_bp
from apps.forms.shop_forms import ShopForm, MenuCateForm, MenusForm
from apps.models import db
from apps.models.shop_models import ShopModel, MenuCateModel, MenusModel
from apps.tools.tools import check_shop_pid


@cms_bp.route("/show/", methods=["GET", "POST"], endpoint="商铺列表")
@login_required
def show_list():
    """查看商家列表"""
    user_id = current_user.id
    form = ShopModel.query.filter(ShopModel.seller_id == user_id, ShopModel.is_status == 0).all()
    return render_template("shop-list.html", form=form, flags="商铺列表展示")


@cms_bp.route("/add/", methods=["GET", "POST"], endpoint="商铺添加")
@login_required
def shop_add():
    """添加店铺"""
    form = ShopForm(request.form)
    if request.method == "POST" and form.validate():
        shop = db.session.query(ShopModel).filter_by(id=form.shop_name.data).first()
        if shop is None:
            shop = ShopModel()
            shop.set_form_attr(form.data)
            pub_id = ''.join(str(uuid.uuid4()).split("-"))[:16]
            shop.pub_id = pub_id
            shop.seller_id = current_user.id
            db.session.add(shop)
            db.session.commit()
            return redirect(url_for("cms.商铺列表"))
        form.shop_name.errors.append("该商家已经存在,请更换商家名")
    return render_template("shop-add.html", form=form, flags="添加")


@cms_bp.route("/update/<pub_id>", methods=["GET", "POST"], endpoint="商铺更新")
@login_required
def shop_update(pub_id):
    """商铺更新"""
    form = None
    if request.method == "GET":
        data = check_shop_pid(pub_id)
        form = ShopForm(data=dict(data))
    elif request.method == "POST":
        form = ShopForm(request.form)
        if form.validate():
            shop = ShopModel.query.filter_by(pub_id=pub_id).first()
            shop.set_form_attr(form.data)
            db.session.commit()
            return redirect(url_for("cms.商铺列表"))
    return render_template("shop-add.html", form=form, flags="更新")


@cms_bp.route("/delete/<pub_id>", methods=["GET", "POST"], endpoint="商铺删除")
@login_required
def shop_delete(pub_id):
    shop = ShopModel.query.filter_by(pub_id=pub_id).first()
    shop.is_status = 1
    db.session.commit()
    return redirect(url_for("cms.商铺列表"))


@cms_bp.route("/cate_list/<pub_id>", methods=["GET", "POST"], endpoint="菜品分类展示")
def cate_list(pub_id):
    form = MenuCateModel.query.filter(MenuCateModel.shop_pid == pub_id, MenuCateModel.is_status == 0).all()
    return render_template("cate_list.html", form=form, pub_id=pub_id, flags="分类列表展示")


@cms_bp.route("/cate_add/<pub_id>", methods=["GET", "POST"], endpoint="菜品分类添加")
@login_required
def cate_add(pub_id):
    form = MenuCateForm(request.form)
    if request.method == "POST" and form.validate():
        cate = MenuCateModel()
        cate.shop_pid = pub_id
        cate.set_form_attr(form.data)
        db.session.add(cate)
        db.session.commit()
        return redirect(url_for("cms.商铺列表"))
    return render_template("shop-add.html", form=form, flags="分类添加")


@cms_bp.route("/cate_update/<cate_id>", methods=["GET", "POST"], endpoint="菜品分类更新")
def cate_update(cate_id):
    """菜品分类更新"""
    form = None
    if request.method == "GET":
        data = MenuCateModel.query.filter_by(id=cate_id).first()
        form = MenuCateForm(data=dict(data))
    elif request.method == "POST":
        form = MenuCateForm(request.form)
        if form.validate():
            cate = MenuCateModel.query.filter_by(id=cate_id).first()
            cate.set_form_attr(form.data)
            db.session.commit()
            return redirect(url_for("cms.菜品分类展示", pub_id=cate.shop_pid))
    return render_template("shop-add.html", form=form, flags="菜品分类更新")


@cms_bp.route("/delete_cate/<cate_id>", methods=["GET", "POST"], endpoint="菜品分类删除")
@login_required
def cate_delete(cate_id):
    cate = MenuCateModel.query.filter_by(id=cate_id).first()
    cate.is_status = 1
    db.session.commit()
    return redirect(url_for("cms.菜品分类展示", pub_id=cate.shop_pid))


@cms_bp.route("/menus_list/<pub_id>", methods=["GET", "POST"], endpoint="菜品列表")
def menus_list(pub_id):
    form = MenusModel.query.filter(MenusModel.shop_id == pub_id, MenusModel.is_status == 0).all()
    return render_template("menus_list.html", form=form, pub_id=pub_id, flags="菜品展示")


@cms_bp.route("/menus_add/<pub_id>", methods=["GET", "POST"], endpoint="菜品添加")
@login_required
def menus_add(pub_id):
    shop = ShopModel.query.filter_by(pub_id=pub_id).first()
    form = MenusForm(shop, request.form)
    if request.method == "POST" and form.validate():
        menu = MenusModel()

        # 本地上传
        img = request.files.get("goods_img")
        name = img.filename
        img.save(name)

        # 服务器到七牛云
        # file = request.files.get("goods_img")
        # access_key = 'A3VIwn1FYmz0pvzT2t5GVZqzRmaBsN4NUg9xzM0g'
        # secret_key = 'RCd_cUofd0Zx1uo8dbZcJidcJsB4PlEtwsC16v8G'
        # q = Auth(access_key=access_key, secret_key=secret_key)
        # token = q.upload_token('elm1106')
        # ret, info = put_data(up_token=token, key=None, data=file.read())

        menu.shop_id = pub_id
        menu.set_form_attr(form.data)
        db.session.add(menu)
        db.session.commit()
        return redirect(url_for("cms.菜品列表", pub_id=pub_id))
    return render_template("shop-add.html", form=form, flags="菜品添加")


@cms_bp.route("/menus_update/<pub_id>/<menu_id>", methods=["GET", "POST"], endpoint="菜品更新")
@login_required
def menus_update(pub_id, menu_id):
    form = None
    shop = ShopModel.query.filter_by(pub_id=pub_id).first()
    if request.method == "GET":
        data = MenusModel.query.filter_by(id=menu_id).first()
        form = MenusForm(shop, data=dict(data))
        goods_img = data.goods_img
    elif request.method == "POST":
        form = MenusForm(shop, request.form)
        if form.validate():
            menu = MenusModel.query.filter_by(id=menu_id).first()
            menu.set_form_attr(form.data)
            db.session.commit()
            return redirect(url_for("cms.菜品列表", pub_id=menu.shop_id))
    return render_template("shop-add.html", form=form, pub_id=pub_id, goods_img=goods_img, flags="菜品更新")


@cms_bp.route("/delete_menu/<pub_id>/<menu_id>", methods=["GET", "POST"], endpoint="菜品删除")
@login_required
def cate_delete(pub_id, menu_id):
    menu = MenusModel.query.filter_by(id=menu_id).first()
    menu.is_status = 1
    db.session.commit()
    return redirect(url_for("cms.菜品列表", pub_id=pub_id))


@cms_bp.route('/uptoken/')
def uptoken():
    access_key = 'A3VIwn1FYmz0pvzT2t5GVZqzRmaBsN4NUg9xzM0g'
    secret_key = 'RCd_cUofd0Zx1uo8dbZcJidcJsB4PlEtwsC16v8G'

    q = Auth(access_key=access_key, secret_key=secret_key)
    token = q.upload_token('elm1106')
    return jsonify({"uptoken": token})
