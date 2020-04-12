from flask import Blueprint, render_template, g, request, redirect, url_for
from werkzeug.exceptions import abort

from routes.auth import login_required
from database import db, User, Item

bp = Blueprint('items', __name__)


@bp.route('/')
@login_required
def index():

    items = []

    if g.user:
        items = Item.query.filter_by(user_id=g.user.id).all() or []

    return render_template('index.html', items=items)


@bp.route('/additem', methods=('POST',))
@login_required
def add_item():

    desc = request.form.get('description')

    if not desc:
        abort(400)

    completed = True if request.form.get('completed') else False

    item = Item(
        user_id=g.user.id,
        description=desc,
        completed=completed
    )
    db.session.add(item)
    db.session.commit()

    return redirect(url_for('index'))


@bp.route('/<int:id>/update', methods=('POST',))
@login_required
def update(id):

    item = Item.query.filter_by(id=id).first()

    if item is None:
        abort(404)

    if g.user.id != item.user_id:
        abort(403)

    desc = request.form.get(f'description-{id}')

    if desc:
        item.description = desc

    completed = True if request.form.get(f'completed-{id}') else False

    if completed is not item.completed:
        item.completed = completed

    db.session.commit()

    return redirect(url_for('index'))


@bp.route('/<int:id>/remove', methods=('POST',))
@login_required
def remove(id):

    user = User.query.filter_by(id=g.user.id).first()
    item = Item.query.filter_by(id=id).first()

    if not item:
        abort(404)

    if user.id != item.user_id:
        abort(403)

    db.session.delete(item)
    db.session.commit()

    return redirect(url_for('index'))
