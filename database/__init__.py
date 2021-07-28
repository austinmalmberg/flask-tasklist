from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True, nullable=False)
    pw_hash = db.Column(db.String(120), nullable=False)

    tasklists = db.relationship('Tasklist', back_populates='user')

    def __init__(self, email, pw_hash):
        self.email = email
        self.pw_hash = pw_hash

    def __repr__(self):
        return f'<User {self.email}>'


class Tasklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), default='New List')
    hide_completed = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='tasklists')

    items = db.relationship('Item', back_populates='tasklist')

    def __init__(self,
                 user_id=None,
                 name=None,
                 hide_completed=None,
                 items=None):
        if user_id is not None:
            self.user_id = user_id
        if name:
            self.name = name
        if hide_completed is not None:
            self.hide_completed = hide_completed
        if items is not None:
            self.items = items

    def __repr__(self):
        return f'<Tasklist {self.name} (owned by {self.user_id})>'


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    tasklist_id = db.Column(db.Integer, db.ForeignKey('tasklist.id'))
    tasklist = db.relationship('Tasklist', back_populates='items')

    def __init__(self,
                 tasklist_id=None,
                 description=None,
                 completed=None):
        if tasklist_id is not None:
            self.tasklist_id = tasklist_id
        if description:
            self.description = description
        if completed is not None:
            self.completed = completed

    def __repr__(self):
        return f'<Item {self.description} ({self.completed})>'
