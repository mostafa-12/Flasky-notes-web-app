from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Regexp
from app.models import User
from app.extensions import hasher_bcrypt
from app.extensions import ALLOWED_IMAGE_EXTENSIONS


class SignUpForm(FlaskForm):
    pic = FileField(label="Profile Picture (Optional)", validators=[FileAllowed(ALLOWED_IMAGE_EXTENSIONS, "Please upload a valid profile picture.")])
    username = StringField("Username", validators=[DataRequired(),
                                                   Regexp(r'^[a-zA-Z0-9_]+$',
                                                          message="Username must contain only letters, numbers, and underscores")])
    email = EmailField("Email", validators=[Email(), DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    re_password = PasswordField("rewrite password again", validators=[EqualTo("password"), DataRequired()])
    remember_me = BooleanField("Remember me in the next time ?")
    submit = SubmitField("SignUp")

    def validate_username(self,username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError("This username is already taken, please choose another one")
        
    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError("This email is already taken by an account, please choose anther one")
    
    
class LogInForm(FlaskForm):
    email = EmailField("Email", validators=[Email(), DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me in the next time ?")
    submit = SubmitField("LogIn")
    
    def validate_email(self,email):
        self.user = User.query.filter_by(email = email.data).first()
        if not self.user:
            raise ValidationError("There is no account with this mail")
        
    def validate(self, extra_validators = None):
        if not super().validate(extra_validators):
            return False
        
        if not self.user.verify_password(self.password.data):
            self.password.errors.append("Invalid password, please try again")
            return False
        
        return True
        
        
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    submit = SubmitField('Change Password')

    def validate_current_password(self, current_password):
        if self.new_password.data:
            if not hasher_bcrypt.verify_input(current_password.data, current_user.hashed_password):
                raise ValidationError('Current password is incorrect. Please enter the correct password to change it.')