from functools import wraps

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    session,
    g,
)
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError

from .db import get_db
from .models import User

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["new-password"]

        error = None
        if not email:
            error = "Email is required"
        elif not password:
            error = "Password is required"

        if error is None:
            db = get_db()

            try:
                db.add(
                    User(
                        email=email,
                        password_hash=generate_password_hash(password),
                    )
                )
                db.commit()
            except IntegrityError:
                error = "User already registered with that email"
            else:
                return redirect(url_for("auth.login"))

        flash(error)
    return render_template("register.j2")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            sa.select(User).where(User.email == email)
        ).scalar_one_or_none()

        error = None
        if user is None:
            error = "Incorrect username"

        elif not check_password_hash(user.password_hash, password):
            error = "Incorrect password"

        if error is None:
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("home.index"))

        flash(error)

    return render_template("login.j2")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home.index"))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        db = get_db()
        g.user = db.execute(
            sa.select(User).where(User.id == user_id)
        ).scalar_one_or_none()


def login_required(view):

    # Important to include @wraps so that flask
    # routing works properly
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view


@login_required
@bp.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        form = request.form
        print(form)

        db = get_db()
        match form:
            case {"display-name": display_name}:
                print(f"{display_name = }")
                g.user.display_name = display_name
                db.commit()
            case {"change-email": new_email}:
                print(f"{new_email = }")
            case {"change-password": new_password}:
                print("change password")
                g.user.password_hash = generate_password_hash(new_password)
                db.commit()
            case _:
                print("Unknown form")

    return render_template("account.j2")
