from flask import render_template, request, redirect, url_for, flash
import datetime
from flask_login import login_required, current_user, login_user, logout_user
from app.auth import auth
from app.auth.forms import SignUpForm, LogInForm, ChangePasswordForm
from app.services import user, email
from app.models import User
from app.services.security import change_password_secure, load_DEK2cache

@auth.route("/signup", methods = ["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    
    
    form = SignUpForm()
    if form.validate_on_submit():
        user.create_user(form)
        email.send_verify_token(form.email.data)
        flash("please check your email address to verify your account before login", "info")
        return redirect(url_for("auth.login"))
    return render_template("auth/signup.html", form = form, title = "signup page" , year = datetime.datetime.now().year)
    
    
@auth.route("/login", methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form  = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is None:
            flash("please Login with a valid email", "danger")
            return redirect(url_for(".login"))
        if not user.account_status:
            flash("verify your account first then login", "danger")
            return redirect(url_for(".login"))
        load_DEK2cache(user, form.password.data)
        login_user(user, remember=form.remember_me.data)
        flash("you logged in successfully", "success")
        return redirect(url_for("main.home"))
    return render_template("auth/login.html", form = form, title = "LogIn page", year = datetime.datetime.now().year)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))

@auth.route("/change-password", methods = ["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if change_password_secure(form):
            flash("your password changed successfully", "success")
        else:
            flash("something went wrong in changing your password, please try again", "danger")
        return redirect(url_for("main.home"))
    return render_template("auth/change_password.html", title = "Change Password", year = datetime.datetime.now().year, form = form)