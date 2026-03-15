from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, EmailField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from app.models import User
from app.extensions import hasher_bcrypt, ALLOWED_IMAGE_EXTENSIONS


class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    pic = FileField(label="Profile Picture (Optional)", validators=[FileAllowed(ALLOWED_IMAGE_EXTENSIONS, "Please upload a valid profile picture.")])
    submit = SubmitField('Save Profile')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user and user.id != current_user.id:
            raise ValidationError('Username is already taken. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user and user.id != current_user.id:
            raise ValidationError('Email is already taken. Please choose a different one.')
        
    


class NoteForm(FlaskForm):
    title = StringField('Title', validators=[Length(5, 20)])
    content = TextAreaField("Content", validators=[Length(max=200)])
    pic = FileField("Note Cover", validators=[FileAllowed(ALLOWED_IMAGE_EXTENSIONS)])
    submit = SubmitField("Add Note")