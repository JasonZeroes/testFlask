from flask import Flask


def register_bp(app: Flask):
    from apps.cms import cms_bp
    app.register_blueprint(cms_bp)


def register_db(app: Flask):
    from apps.models import db
    db.init_app(app)


def init_session(app):
    from flask_session import Session
    Session(app)


def init_login_manager(app):
    from apps.tools.login_tools import login_manager
    login_manager.init_app(app)


def register_api_bp(app):
    from apps.apis import api_bp
    app.register_blueprint(api_bp)


def create_app(config_str: str):
    """初始化创建app"""
    app = Flask(__name__, static_folder="./cms_statics", static_url_path="/static")
    # app.add_url_rule()

    # 注册配置文件
    app.config.from_object(config_str)

    # 初始化配置session保存到Redis中
    init_session(app)

    # 注册数据库
    register_db(app)

    # 初始化login_manger
    init_login_manager(app)

    # 注册蓝图
    register_bp(app)

    return app


def create_api_app(config_str: str):
    app = Flask(__name__, static_folder="./web_client", static_url_path="")
    app.config.from_object(config_str)
    register_db(app)
    register_api_bp(app)
    return app
