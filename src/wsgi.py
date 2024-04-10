import os

from flask import Flask, config


def create_app(test_config=None):
    app = Flask(
        __name__,
        instance_relative_config=True,
        instance_path=os.path.join(os.getcwd(), "instance"),
    )
    app.config.from_mapping(
        SECRET_KEY="dev-change-me",
        DB_URL=f"sqlite:///{os.path.join(app.instance_path, 'db.sqlite')}",
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    # Register views / blueprints
    from . import auth, home

    app.register_blueprint(home.bp)
    app.register_blueprint(auth.bp)

    # Make sure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        # Already exists
        pass

    from . import db

    db.init_app(app)

    return app
