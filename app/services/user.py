from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError
from app.services.security import create_user_keys, save_pics_secure
from app.extensions import db
from app.models import User
from app.auth.forms import SignUpForm
from app.main.forms import UpdateProfileForm



def create_user(form : SignUpForm):
    user = User.query.filter_by(email = form.email.data).first()
    if user:
        print(f" error in creating user, {user.name} is already registered in database")
        raise IntegrityError
    user_DEK, KEK_salt = create_user_keys(form.password.data)
    # init base User instance
    user = User(
        username = form.username.data,
        email = form.email.data,
        KEK_salt = KEK_salt,
        DEK_encrypted = user_DEK
    )
    user.password = form.password.data

    # init user profile picture

    user.profile_pic = save_pics_secure(form)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as err:
        db.session.rollback()
        print(f" error in creating user, {err}")

    print("create user success")
    return True


    
def delete_user(user: User):
    try:
        db.session.delete(user)
        db.session.commit
    except Exception as err:
        db.session.rollback()
        print(f" error in deleting user, {err}")  
        

def update_user(form : UpdateProfileForm):
    user = User.query.filter_by(email = form.email.data).first()
    if user:
        if current_user.id != user.id:
            print(f" error in updating user, {user.name} is not the current user")
            raise IntegrityError
    user = current_user
    user.username = form.username.data
    user.email = form.email.data
    user.profile_pic = save_pics_secure(form)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as err:
        db.session.rollback()
        print(f" error in updating user, {err}")
        return False
    
    return True
    