from flask import Blueprint, request, redirect, url_for, flash, render_template, session
from werkzeug.security import check_password_hash, generate_password_hash

from database import commit
from database.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        error = None

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif User.query.filter_by(email=email).first() is not None:
            error = f"Email address '{email}' is already registered."

        if error is None:
            user = User(email, generate_password_hash(password))
            commit(user)
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        error = None

        user = User.query.filter_by(email=email).first()

        if user is None:
            error = 'Incorrect email.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')