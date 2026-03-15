from flask import Flask, g, redirect, flash, request, url_for
from flask_login import current_user, logout_user
from app.extensions import db, login_manager, mail, hasher_bcrypt
from config import configs
from app.models import User
from app.main import main
from app.auth import auth
from app.email import Email
from sec_layer.encrypt import FernetEncrypt
PUBLIC_ENDPOINTS = {"auth.login", "auth.signup", "main.home", "email.verification", "static"}

def create_app(config_name = "develop"):
    app = Flask(__name__)
    app.config.from_object(configs[config_name])
    configs[config_name].init_app(app)
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(Email)
    app.DEK_KEYs = {}
    # init app for extensions
    db.init_app(app)
    #login manager and it's configs
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "you must be logged in to access this page"
    login_manager.login_message_category = "info"
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    #mailman initialize
    mail.init_app(app) 
    # get DEK for current user before his request
    @app.before_request
    def load_user_DEK():
        if request.endpoint in PUBLIC_ENDPOINTS:
                return
        if not current_user.is_authenticated:
            flash("unexpected error, please login again")
            return redirect(url_for("auth.login"))
        dek = app.DEK_KEYs.get(current_user.id)
        if dek is None:
            logout_user()
            flash("unexpected error, please login again")
            return redirect(url_for("auth.login"))
        g.dek = dek
        
    # set Encrypt object for every request
    @app.before_request
    def set_encrypt():
        if request.endpoint in PUBLIC_ENDPOINTS:
                return
        if hasattr(g, "dek"):
            g.encrypt = FernetEncrypt(g.dek)
            
        else:
            logout_user()
            flash("unexpected error, please login again")
            return redirect(url_for("auth.login"))
    return app