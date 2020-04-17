from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True, nullable=False)
    pw_hash = db.Column(db.String(120), nullable=False)

    lists = db.relationship('TodoList')

    def __repr__(self):
        return f'<User {self.email}>'


class TodoList(db.Model):
    __tablename__ = 'todolist'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(60), default='New List')

    items = db.relationship('Item')

    def __repr__(self):
        return f'<List {self.name} (owned by {self.user_id})>'


class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('todolist.id'))
    description = db.Column(db.String(80), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Item {self.description} ({self.completed})>'
