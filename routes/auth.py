import functools

from flask import Blueprint, request, redirect, url_for, flash, render_template, session, g
from werkzeug.security import check_password_hash, generate_password_hash

from database import db, User, TaskList, Item

bp = Blueprint('auth', __name__)

register_tasklist = TaskList(name='Things to do', items=[
    Item(description='Register', completed=False),
    Item(description='Login', completed=False),
    Item(description='Organize your workflow', completed=False)
])

login_tasklist = TaskList(name='Things to do', items=[
    Item(description='Register', completed=True),
    Item(description='Login', completed=False),
    Item(description='Organize your workflow', completed=False)
])


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        error = None

        if not email:
            error = 'Email is required'
        elif User.query.filter_by(email=email).first() is not None:
            error = f"Email address is already registered"
        elif not password:
            error = 'Password is required'
        elif not confirm_password or password != confirm_password:
            error = 'Passwords do not match'

        if error is None:
            user = User(
                email=email,
                pw_hash=generate_password_hash(password)
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))

        flash(error, 'error')

    return render_template('auth/register.html', tasklist=register_tasklist)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        error = None

        if user is None:
            error = 'Invalid email'
        elif not check_password_hash(user.pw_hash, password):
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))

        flash(error, 'error')

    return render_template('auth/login.html', tasklist=login_tasklist)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
