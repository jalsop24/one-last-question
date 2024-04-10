import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker

from flask import current_app, g, Flask


def get_db() -> scoped_session:
    if "db" not in g:
        engine = sa.create_engine(
            current_app.config["DB_URL"],
        )
        session = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=engine,
            )
        )
        g.db = session
    return g.db


def close_db(e=None):
    session: scoped_session | None = g.pop("db", None)

    if session is not None:
        session.remove()


def init_app(app: Flask):
    app.teardown_appcontext(close_db)
