from flask import render_template, redirect, request, flash, session
from app import app, utils, models, db
from .forms import LoginForm
import hashlib


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user', None) is not None:
        return render_template('index.html',
                               title='Home',
                               user=models.User.query.get(session['user']))
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
    return render_template('index.html',
                           title='Home',
                           user=user)


@app.route('/create', methods=['POST'])
def validate_create():
    print(request, request.form)
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
    return render_template('index.html',
                           title='Home',
                           user=u)


@app.route('/logout')
def logout():
    session['user'] = None
    return redirect('/login')
