import functools

from flask import Blueprint, render_template, g, request, Response
from werkzeug.exceptions import abort

from database import db, TaskList, Item
from routes.auth import login_required

bp = Blueprint('tasklist', __name__)

max_input_length = 26


def authorize_list_action(view):
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
        tasklist = TaskList.query.filter_by(id=kwargs['list_id']).first()

        if tasklist is None:
            abort(404)
        elif g.user.id != tasklist.user_id:
            abort(403)

        return view(**kwargs, tasklist=tasklist)

    return wrapped_view


@bp.route('/')
@login_required
def index():
    tasklists = []

    if g.user:
        tasklists = TaskList.query.filter_by(user_id=g.user.id).all() or []

    return render_template('index.html', max_length=max_input_length, tasklists=tasklists)


@bp.route('/create', methods=('POST',))
@login_required
def create():
    tasklist = TaskList(
        user_id=g.user.id
    )

    db.session.add(tasklist)
    db.session.commit()

    return render_template('tasklist/tasklist.html', tasklist=tasklist)


@bp.route('/<int:list_id>/update', methods=('POST',))
@login_required
@authorize_list_action
def update(list_id, tasklist):
    new_name = request.form.get(f'task--name')

    if new_name and len(new_name.strip()) > 0:
        tasklist.name = new_name[:max_input_length]

        db.session.commit()

        return render_template('tasklist/tasklist_header.html', tasklist=tasklist)

    return Response(
        response='A list title is required',
        status=400
    )


@bp.route('/<int:list_id>/delete', methods=('POST',))
@login_required
@authorize_list_action
def delete(list_id, tasklist):
    list_items = Item.query.filter_by(list_id=list_id).all()

    for item in list_items:
        db.session.delete(item)

    db.session.delete(tasklist)
    db.session.commit()

    return Response(status=200)


@bp.route('/<int:list_id>/additem', methods=('POST',))
@login_required
@authorize_list_action
def add_item(list_id, tasklist):
    description = request.form.get('description')

    if description:
        completed = True if request.form.get('completed') else False

        item = Item(
            list_id=tasklist.id,
            description=description[:max_input_length],
            completed=completed
        )

        db.session.add(item)
        db.session.commit()

        return render_template('tasklist/item.html', tasklist=tasklist, item=item)

    return Response(
        response='A description is required',
        status=400
    )


@bp.route('/<int:list_id>/<int:item_id>/update', methods=('POST',))
@login_required
@authorize_list_action
def update_item(list_id, item_id, tasklist):
    item = Item.query.filter_by(id=item_id).first()

    # make sure the item exists
    if item is None:
        abort(404)

    description = request.form.get('description')

    if description:
        item.description = description[:max_input_length]

        completed = True if request.form.get('completed') else False

        # update completed only if the state changed (probably not needed)
        if completed is not item.completed:
            item.completed = completed

        db.session.commit()

        return render_template('tasklist/item.html', tasklist=tasklist, item=item)

    return Response(
        response='A description is required',
        status=400
    )


@bp.route('/<int:list_id>/<int:item_id>/delete', methods=('POST',))
@login_required
@authorize_list_action
def remove(list_id, item_id, tasklist):
    item = Item.query.filter_by(id=item_id).first()

    if not item:
        abort(404)

    db.session.delete(item)
    db.session.commit()

    return Response(status=200)
