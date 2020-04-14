from flask import Blueprint, render_template, g, request, redirect, url_for, flash
from werkzeug.exceptions import abort

from routes.auth import login_required
from database import db, TodoList, Item

bp = Blueprint('items', __name__)


@bp.route('/')
@login_required
def index():
    todolists = []

    if g.user:
        todolists = TodoList.query.filter_by(user_id=g.user.id).all() or []

    return render_template('index.html', todolists=todolists)


@bp.route('/create', methods=('POST',))
@login_required
def create():
    todolist = TodoList(
        user_id=g.user.id
    )

    db.session.add(todolist)
    db.session.commit()

    return redirect(url_for('index'))


@bp.route('/<int:list_id>/update', methods=('POST',))
@login_required
def update(list_id):
    new_name = request.form.get(f'todo-{list_id}--title')

    if not new_name:
        flash('A list title is required', f'list-{list_id}')

    else:
        todolist = TodoList.query.filter_by(id=list_id).first()

        if todolist is None:
            abort(404)

        if g.user.id != todolist.user_id:
            abort(403)

        todolist.name = new_name

        db.session.commit()

    return redirect(url_for('index'))


@bp.route('/<int:list_id>/delete', methods=('POST',))
@login_required
def delete(list_id):
    todolist = TodoList.query.filter_by(id=list_id).first()

    # make sure the list exists
    if todolist is None:
        abort(404)

    # make sure it belongs to the logged in user
    if g.user.id != todolist.user_id:
        abort(403)

    list_items = Item.query.filter_by(list_id=list_id).all()

    for item in list_items:
        db.session.delete(item)

    db.session.delete(todolist)
    db.session.commit()

    return redirect(url_for('index'))


@bp.route('/<int:list_id>/additem', methods=('POST',))
@login_required
def add_item(list_id):
    desc = request.form.get('description')

    if not desc:

        flash('A description is required', f'list-{list_id}')

    else:

        completed = True if request.form.get('completed') else False

        item = Item(
            list_id=list_id,
            description=desc,
            completed=completed
        )
        db.session.add(item)
        db.session.commit()

    return redirect(url_for('index'))


@bp.route('/<int:list_id>/<int:item_id>/update', methods=('POST',))
@login_required
def update_item(list_id, item_id):
    todolist = TodoList.query.filter_by(id=list_id).first()

    # make sure the item exists
    if todolist is None:
        abort(404)

    # make sure the todolist belongs to the logged in user
    if g.user.id != todolist.user_id:
        abort(403)

    item = Item.query.filter_by(id=item_id).first()

    # make sure the item exists
    if item is None:
        abort(404)

    desc = request.form.get(f'description-{item_id}')

    if desc:
        item.description = desc

    completed = True if request.form.get(f'completed-{item_id}') else False

    # update completed only if the state changed (probably not needed)
    if completed is not item.completed:
        item.completed = completed

    db.session.commit()

    return redirect(url_for('index'))


@bp.route('/<int:list_id>/<int:item_id>/remove', methods=('POST',))
@login_required
def remove(list_id, item_id):
    todolist = TodoList.query.filter_by(id=list_id).first()

    if not todolist:
        abort(404)

    if g.user.id != todolist.user_id:
        abort(403)

    item = Item.query.filter_by(id=item_id).first()

    if not item:
        abort(404)

    db.session.delete(item)
    db.session.commit()

    return redirect(url_for('index'))
