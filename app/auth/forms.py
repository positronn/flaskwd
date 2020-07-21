# app/auth/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators = [DataRequired(), Length(1, 64), Email()]
    )

    password = PasswordField(
        'Password',
        validators = [DataRequired()]
    )

    remember_me = BooleanField(
        'Keep me logged in'
    )

    submit = SubmitField(
        'Log in'
    )


class RegistrationForm(FlaskForm):
    email = StringField(
        'Email',
        validators = [DataRequired(), Length(1, 64), Email()]
    )

    # regex for asserting valid username, used in definition of username
    regex = Regexp(
        '^[A-Za-z][A-Za-z0-9_.]*$',
        flags = 0,
        message = 'Usernames must have only letters, numbers, dots or underscores'
    )

    username = StringField(
        'Username',
        validators = [DataRequired(), Length(1, 64), regex]
    )

    password = PasswordField(
        'Password',
        validators = [DataRequired(), EqualTo('password2', message = 'Passwords must match')]
    )

    password2 = PasswordField(
        'Confirm password',
        validators = [DataRequired()]
    )

    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Email already registered.')
    
    def validate_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('Username already in use.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(
        'Old Password',
        validators = [DataRequired()]
    )

    password = PasswordField(
        'New Password',
        validators = [DataRequired(), EqualTo('password2', message = 'Passwords must match.')]
    )

    password2 = PasswordField(
        'Confirm new password',
        validators = [DataRequired()]
    )

    submit = SubmitField('Update Password')


class PasswordResetRequestForm(FlaskForm):
    email = StringField(
        'Email',
        validators = [DataRequired(), Length(1, 64), Email()]
    )

    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    password = PasswordField(
        'New Password',
        validators = [DataRequired(), EqualTo('password2', message = 'Passwords must match')]
    )

    password2 = PasswordField(
        'Confirm Password',
        validators = [DataRequired()]
    )

    submit = SubmitField('Reset Password')
