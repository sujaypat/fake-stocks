from flask import render_template, redirect, request, flash, session
from app import app, utils, db
from .forms import LoginForm, TransactionForm
from app.utils import *
import hashlib


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user', None) is not None:
        form = TransactionForm()
        return render_template('index.html',
                               title='Home',
                               user=models.User.query.get(session['user']),
                               form=form)
    form = LoginForm()
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/submit', methods=['POST'])
def validate_login():
    user = utils.read_user_from_db(request.form['username'], request.form['password'])
    if not user:
        flash("incorrect username or password")
        return redirect('/login')
    print('about to save user')
    session['user'] = user.username
    form = TransactionForm()
    return render_template('index.html',
                           title='Home',
                           user=user,
                           form=form)


@app.route('/create', methods=['POST'])
def validate_create():
    # print(request, request.form)
    u = None
    if not utils.username_exists(request.form['create_username']):
        u = models.User(username=request.form['create_username'],
                        password=hashlib.sha512(request.form['create_password'].encode('utf-8')).digest(),
                        bank_balance=0)
        db.session.add(u)
        db.session.commit()
    else:
        flash("username already exists")
        return redirect('/login')
    session['user'] = u.username
    form = TransactionForm()
    return render_template('index.html',
                           title='Home',
                           user=u,
                           form=form)


@app.route('/logout')
def logout():
    session['user'] = None
    return redirect('/login')


@app.route('/buy', methods=['POST'])
def buy_stock():
    """
    :param username: username of purchaser
    :param ticker: stock symbol
    :param num_shares: number of shares desired
    :return: True if purchase is valid
    """
    form = TransactionForm()
    u = username_exists(session['user'])
    price = get_current_price(form.buy_ticker.data)
    if not u:
        return redirect('/')

    shares = models.Share.query.filter_by(ticker=form.buy_ticker.data.lower()).first()
    print(shares)
    if not shares:
        s = models.Share(ticker=form.buy_ticker.data.lower(), count=int(form.buy_num.data), user_id=u.id)
        u.bank_balance -= price * int(form.buy_num.data)
        db.session.add(s)
        db.session.commit()
        return redirect('/')

    if u.bank_balance >= price*int(form.buy_num.data):
        shares.count += int(form.buy_num.data)
        u.bank_balance -= price*int(form.buy_num.data)
        db.session.commit()
    else:
        flash('insufficient funds')
    return redirect('/')


@app.route('/sell', methods=['POST'])
def sell_stock():
    """
    :param username: username of seller
    :param ticker: stock symbol
    :param num_shares: number of shares to sell
    :return: True if sale is valid
    """
    form = TransactionForm()
    u = username_exists(session['user'])
    price = get_current_price(form.sell_ticker.data)
    if not u:
        return False

    shares = models.Share.query.filter_by(ticker=form.sell_ticker.data.lower()).first()
    print(shares)
    if not shares:
        flash('you do not own this stock')
        return redirect('/')

    if shares.count >= int(form.sell_num.data):
        shares.count -= int(form.sell_num.data)
        u.bank_balance += price * int(form.sell_num.data)
        db.session.commit()
    else:
        flash('you do not own enough of this stock')
    return redirect('/')


@app.route('/funds', methods=['POST'])
def add_remove_funds():

    form = TransactionForm()
    u = username_exists(session['user'])
    if not u:
        return False

    u.bank_balance += int(form.funds_amt.data)
    db.session.commit()
    return redirect('/')
