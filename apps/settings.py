import os

from redis import Redis


def get_db_path():
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return f"sqlite:///{path}/Elm.db"


def get_redis_address():
    return Redis(host="127.0.0.1", port=6379)


class DevConfig:
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = get_db_path()
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevCMSConfig(DevConfig):
    SESSION_TYPE = "redis"
    SESSION_REDIS = get_redis_address()
    SESSION_KEY_PREFIX = "2019:"

    WTF_CSRF_SECRET_KEY = "wtf_abc"


class DevApiConfig(DevConfig):
    SECRET_KEY = "Elm_api"
    SMS_LIFETIME = 120
    API_REDIS = get_redis_address()
    TOKEN_EXPIRES = 24 * 3600
    CART_LIFETIME = 3600
