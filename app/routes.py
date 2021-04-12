from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app import utility
from app.forms import LoginForm, RegistrationForm, TransactionForm
from app.models import User


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index')
@login_required
def index():
    transactions = utility.get_transactions(current_user.id)
    return render_template('index.html', title='Home', transactions=transactions)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        utility.user_verification_task(form.username.data)
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/transaction', methods=['GET', 'POST'])
@login_required
def transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        user_id = current_user.id
        amount = form.amount.data
        current_balance = current_user.current_balance
        if current_user.is_verified == 1:
            utility.add_transaction(user_id, amount, current_balance)        
            flash('Congratulations, Transaction Complete!')
        elif current_user.is_verified == -1:
            flash('invalid username must not contain special char')
        else:
            flash('profile not verified')
        return redirect(url_for('index'))
    return render_template('transaction.html', title='Transaction', form=form)


@app.route('/reverify')
@login_required
def reverify():
    utility.user_verification_task(current_user.username)
    return redirect(url_for('index'))
