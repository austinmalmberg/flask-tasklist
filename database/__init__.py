from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    db.init_app(app)


def commit(instance):
    db.session.add(instance)
    db.session.commit()