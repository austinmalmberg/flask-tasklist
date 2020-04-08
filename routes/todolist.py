import json

from flask import Blueprint, render_template, g, request, redirect, url_for, Response
from werkzeug.exceptions import abort

from routes.auth import login_required
from database import db, User, Item

bp = Blueprint('items', __name__)


@bp.route('/')
def index():

    items = []

    if g.user:
        items = Item.query.filter_by(user_id=g.user.id).all()

    return render_template('index.html', items=items or [])


@bp.route('/additem', methods=('POST',))
@login_required
def create():
    if request.method == 'POST':

        json_data = request.get_json()

        desc = json_data.get('description')

        if not desc:
            abort(400)

        item = Item(
            user_id=g.user.id,
            description=desc,
            completed=False
        )
        db.session.add(item)
        db.session.commit()

        return render_template('snippets/item.html', item=item)


@bp.route('/<int:id>/update', methods=('POST',))
@login_required
def update(id):

    item = Item.query.filter_by(id=id).first()

    if item is None:
        abort(404)

    json_data = request.get_json()

    desc = json_data.get('description')
    completed = json_data.get('completed')

    if g.user.id != item.user_id:
        abort(403)

    if not desc and not completed:
        abort(400)

    if desc:
        item.description = desc

    if completed and isinstance(completed, bool):
        item.completed = completed

    db.session.commit()

    return render_template('snippets/item.html', item=item)


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

    return Response(status=200)


@bp.route('/emptyitem', methods=('GET',))
def empty_item():
    return render_template('snippets/item.html')
