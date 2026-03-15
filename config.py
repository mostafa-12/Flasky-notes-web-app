import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class BaseConfig:
    @staticmethod
    def init_app(app):
        pass

class DevConfig(BaseConfig):
    FLASK_POSTS_PER_PAGE = 10
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'DEV_db.sqlite3')
    FLASK_MAIL_SENDER = "mos095tafa@gmail.com"
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'mos095tafa@gmail.com'
    MAIL_PASSWORD = 'cpuq turp pekb msqd'
    SECRET_KEY = "dev SECRET KEY"
    DEBUG = True



configs = {
    "base" : BaseConfig,
    'develop': DevConfig,
    'default': DevConfig
}