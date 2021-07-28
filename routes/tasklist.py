import functools

from flask import Blueprint, render_template, g, request, Response
from werkzeug.exceptions import abort

from database import db, Tasklist, Item
from routes.auth import login_required

bp = Blueprint('tasklist', __name__)

MAX_INPUT_LENGTH = 36


def authorize_tasklist_action(view):
    """
    A view decorator that
        1) verifies the tasklist exists, and
        2) verifies the user that's currently logged in has authorization to change the list

    In cases where one of these are not correct, the decorator will (respectively)
        1) abort with a 404 Not Found status, or
        2) abort with a 403 Forbidden status

    If the tasklist is owned by the logged in user, the tasklist kwarg is passed onto the view. This prevents having to
    query the database again if it's used in the view method.

    This decorator will throw an error if list_id is not provided as a kwarg

    :param view: the view method. An error is thrown if list_id is omitted from the kwargs
    :return: the view with the tasklist passed as a kwarg
    """

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        id = kwargs.get('tasklist_id', None)

        if id is None:
            return abort(400)

        g.tasklist = Tasklist.query.get(id)

        if g.tasklist is None:
            return abort(404)
        elif g.user.id != g.tasklist.user_id:
            return abort(403)

        return view(**kwargs)

    return wrapped_view


@bp.route('/')
@login_required
def index():
    tasklists = []

    if g.user:
        tasklists = Tasklist.query.filter_by(user_id=g.user.id).order_by(Tasklist.id).all() or []

    return render_template('index.html', max_length=MAX_INPUT_LENGTH, tasklists=tasklists)


@bp.route('/create', methods=('POST',))
@login_required
def create():
    tasklist = Tasklist(
        user_id=g.user.id
    )

    db.session.add(tasklist)
    db.session.commit()

    return render_template('tasklist/tasklist.html', tasklist=tasklist)


@bp.route('/<int:tasklist_id>/update', methods=('POST',))
@login_required
@authorize_tasklist_action
def update(tasklist_id):
    new_name = request.form.get(f'task__name')

    if new_name and len(new_name.strip()) > 0:
        g.tasklist.name = new_name[:MAX_INPUT_LENGTH]

        db.session.commit()

        return render_template('tasklist/_header.html', tasklist=g.tasklist)

    return Response(
        response='A list title is required',
        status=400
    )


@bp.route('/<int:tasklist_id>/delete', methods=('POST',))
@login_required
@authorize_tasklist_action
def delete(tasklist_id):
    list_items = Item.query.filter_by(tasklist_id=tasklist_id).all()

    for item in list_items:
        db.session.delete(item)

    db.session.delete(g.tasklist)
    db.session.commit()

    return Response(status=200)


@bp.route('/<int:tasklist_id>/additem', methods=('POST',))
@login_required
@authorize_tasklist_action
def add_item(tasklist_id):
    description = request.form.get('description')

    if description:
        completed = True if request.form.get('completed') else False

        item = Item(
            tasklist_id=g.tasklist.id,
            description=description[:MAX_INPUT_LENGTH],
            completed=completed
        )

        db.session.add(item)
        db.session.commit()

        return render_template('tasklist/item.html', tasklist=g.tasklist, item=item)

    return Response(
        response='A description is required',
        status=400
    )


@bp.route('/<int:tasklist_id>/<int:item_id>/update', methods=('POST',))
@login_required
@authorize_tasklist_action
def update_item(tasklist_id, item_id):
    item = Item.query.filter_by(id=item_id).first()

    # make sure the item exists
    if item is None:
        return abort(404)

    description = request.form.get('description')

    if description:
        item.description = description[:MAX_INPUT_LENGTH]

        completed = True if request.form.get('completed') else False

        # update completed only if the state changed (probably not needed)
        if completed is not item.completed:
            item.completed = completed

        db.session.commit()

        return render_template('tasklist/item.html', tasklist=g.tasklist, item=item)

    return Response(
        response='A description is required',
        status=400
    )


@bp.route('/<int:tasklist_id>/<int:item_id>/delete', methods=('POST',))
@login_required
@authorize_tasklist_action
def remove(tasklist_id, item_id):
    item = Item.query.filter_by(id=item_id).first()

    if not item:
        return abort(404)

    db.session.delete(item)
    db.session.commit()

    return Response(status=200)
