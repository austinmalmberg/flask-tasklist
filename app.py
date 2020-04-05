import os

from flask import Flask


def create_app():

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        DATABASE=os.environ.get('DATABASE_URL', os.path.join(app.instance_path, 'todo.sqlite'))
    )

    @app.route('/')
    def index():
        return 'Hello, world!'

    return app