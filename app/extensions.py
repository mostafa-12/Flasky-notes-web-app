from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mailman import Mail
import os
from sec_layer.hash import Hash_bcrypt
APP_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
hasher_bcrypt = Hash_bcrypt()

ALLOWED_IMAGE_EXTENSIONS = [
     "jpg","jpeg","png","gif","webp","bmp","tiff","tif",
    "svg","ico","heic","heif","avif","jfif","pjpeg","pjp"
]