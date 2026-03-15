import os, base64
from flask import current_app as app
from flask_login import current_user
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from app.models import User
from app.extensions import APP_ROOT_PATH
from app.extensions import hasher_bcrypt, db
from sec_layer.encrypt import FernetEncrypt
def create_user_keys(password: str, random_user_key = None):
    # user security layer
    random_user_key = base64.b64encode(os.urandom(32)) if random_user_key is None else random_user_key
    kdf = hasher_bcrypt.make_kdf(password)
    FernetEncryptor = FernetEncrypt(kdf[2])
    KEK_salt = kdf[0]
    user_DEK = FernetEncryptor.encrypt(random_user_key)

    return user_DEK, KEK_salt


def save_pics_secure(form : FlaskForm):
    pic = form.pic.data
    if not pic:
        print("no profile pic provided")
        return None
    pics_path = os.path.join(APP_ROOT_PATH, 'static', 'pics')
    if not os.path.exists(pics_path):
        os.makedirs(pics_path)
    pic = form.pic.data
    pic_name = secure_filename(hasher_bcrypt.hash_input(pic.filename).decode("utf-8")) + os.path.splitext(pic.filename)[1]
    pic.save(os.path.join(pics_path, pic_name))
    print("saving profile_pic successfully")
    return pic_name

def change_password_secure(form : FlaskForm):
    user = current_user
    KEK_salt = user.KEK_salt
    kdf = hasher_bcrypt.make_kdf(form.current_password.data, KEK_salt)
    FernetEncryptor = FernetEncrypt(kdf[2])
    user_DEK = FernetEncryptor.decrypt(user.DEK_encrypted)
    app.DEK_KEYs[user.id] = user_DEK
    user_DEK_encrypted, user_KEK_salt = create_user_keys(form.new_password.data, user_DEK)
    user.password = form.new_password.data
    user.KEK_salt = user_KEK_salt
    user.DEK_encrypted = user_DEK_encrypted
    db.session.add(user)
    try:
        db.session.commit()
    except Exception as err:
        db.session.rollback()
        print(f" error in changing password, {err}")
        return False
    print("change password successfully")
    return True
        
    
def load_DEK2cache(user: User,password:str):
    KEK_salt = user.KEK_salt
    kdf = hasher_bcrypt.make_kdf(password, KEK_salt)
    FernetEncryptor = FernetEncrypt(kdf[2])
    user_DEK = FernetEncryptor.decrypt(user.DEK_encrypted)
    app.DEK_KEYs[user.id] = user_DEK
    return {
        user.id : user_DEK
    }