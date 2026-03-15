from flask import g
from sqlalchemy import event
from flask_login import UserMixin
import datetime
from app.extensions import db, hasher_bcrypt
GET_TIME = lambda: datetime.datetime.now(datetime.timezone.utc)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    email = db.Column(db.String(120), index = True, unique = True, nullable = False)
    hashed_password = db.Column(db.LargeBinary)
    KEK_salt = db.Column(db.LargeBinary)
    DEK_encrypted = db.Column(db.LargeBinary)
    created_at = db.Column(db.DateTime, default= GET_TIME)
    profile_pic = db.Column(db.String, default = "default_profile_pic.png")
    account_status = db.Column(db.Boolean, default = False)
    notes = db.relationship("Note", backref="user", lazy="dynamic")
    
    def verify_password(self, entered_password: str| bytes):
        return hasher_bcrypt.verify_input(entered_password, self.hashed_password)
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')
    @password.setter
    def password(self, password):
        self.hashed_password = hasher_bcrypt.hash_input(password)

    
class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50))
    encrypted_content = db.Column(db.LargeBinary)
    cover_pic = db.Column(db.String, default = "default_note_pic.jpg")
    created_at = db.Column(db.DateTime, default= GET_TIME)
    latest_modified = db.Column(db.DateTime, default= GET_TIME, onupdate= GET_TIME)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @property
    def content(self):
        if self.encrypted_content is not None:
            return g.encrypt.decrypt(self.encrypted_content).decode("utf-8")
        else:
            return None
    @content.setter
    def content(self, value):
        if value is not None:
            self.encrypted_content = g.encrypt.encrypt(value)
        else:
            self.encrypted_content = None

@event.listens_for(Note, 'before_update')
def latest_modified_listener(mapper, conn, instance):
    instance.latest_modified = GET_TIME()