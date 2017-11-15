from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from app import utils


class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')
    submit = SubmitField('submit', )
    create_username = StringField('username')
    create_password = PasswordField('password')
    create_acct = SubmitField('create')
