from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password_confirm', message='Passwords must match'), Length(6, 16)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')
