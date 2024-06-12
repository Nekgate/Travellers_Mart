from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flask_station.models import User

# Form for user registration
class RegistrationForm(FlaskForm):
    # Username field with validators for data requirement and length
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    
    # Email field with validators for data requirement and email format
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    # Password field with a validator for data requirement
    password = PasswordField('Password', validators=[DataRequired()])
    
    # Confirm password field with validators for data requirement and equality to the password field
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    
    # Submit button
    submit = SubmitField('Sign up')

    # Custom validator to check if the username is already taken
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    # Custom validator to check if the email is already registered
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

# Form for user login
class LoginForm(FlaskForm):
    # Email field with validators for data requirement and email format
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    # Password field with a validator for data requirement
    password = PasswordField('Password', validators=[DataRequired()])
    
    # Remember me checkbox field
    remember = BooleanField('Remember Me')
    
    # Submit button
    submit = SubmitField('Login')

# Form for updating account information
class UpdateAccountForm(FlaskForm):
    # Username field with validators for data requirement and length
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    
    # Email field with validators for data requirement and email format
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    # File field for updating profile picture, allowing only specific file types
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    
    # Submit button
    submit = SubmitField('Update')

    # Custom validator to check if the username is already taken, excluding the current username
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    # Custom validator to check if the email is already registered, excluding the current email
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

# Form for requesting a password reset
class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    # Submit button
    submit = SubmitField('Request Password Reset')

    # Custom validator to check if the email is registered
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account for that email. You must register first.')

# Form for resetting the password
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    
    # Submit button
    submit = SubmitField('Reset Password')
