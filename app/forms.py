from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')
    submit = SubmitField('log in')
    create_username = StringField('username')
    create_password = PasswordField('password')
    create_acct = SubmitField('create')


class TransactionForm(FlaskForm):
    funds_amt = StringField('funds_amt')
    funds_submit = SubmitField('submit')

    buy_ticker = StringField('buy_ticker')
    buy_num = StringField('buy_num')
    buy_submit = SubmitField('buy')

    sell_ticker = StringField('sell_ticker')
    sell_num = StringField('sell_num')
    sell_submit = SubmitField('sell')
