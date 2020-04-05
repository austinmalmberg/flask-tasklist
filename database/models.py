from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True, nullable=False)
    pw_hash = db.Column(db.String(120), nullable=False)

    tasks = db.relationship('Task')

    def __repr__(self):
        return f'<User {self.email}>'


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    task_name = db.Column(db.String(80), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.task_name}>'
