import json
import os

from flask import Flask


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
        app.config.from_file("config.json", load=json.load)
    else:
        app.config.from_mapping(test_config)

    # Register views / blueprints
    from . import auth, email, home, newsletters

    email.mail.init_app(app)

    app.register_blueprint(home.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(newsletters.bp)

    # Make sure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        # Already exists
        pass

    from . import db

    db.init_app(app)

    return app
