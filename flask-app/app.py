import os

from flask import Flask, redirect, url_for


def register_blueprints(app):
    @app.route('/')
    def landing_page():
        return redirect(url_for('info.index'))

    from views.info import info

    app.register_blueprint(info, url_prefix='/info')


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_blueprints(app)

    # with app.app_context():
    #     from .views.info import info
    #     app.register_blueprint(info)

    return app
