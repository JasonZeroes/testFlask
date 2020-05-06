from flask_login import LoginManager
from apps.models.user_models import UserModel

login_manager = LoginManager()
login_manager.login_view = 'cms.登录'


@login_manager.user_loader
def load_user(uid):
    return UserModel.query.get(int(uid))
