import os

from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///tasklist.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    import database
    database.init_app(app)

    from routes import tasklist
    app.register_blueprint(tasklist.bp)
    app.add_url_rule('/', endpoint='index')

    from routes import auth
    app.register_blueprint(auth.bp)

    return app
