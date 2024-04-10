from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
)
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy as sa

from .db import get_db
from .models import User

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "GET":
        return render_template("register.j2")
    elif request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        error = None
        if not email:
            error = "Email is required"
        elif not password:
            error = "Password is required"

        if error is None:
            db = get_db()

            db.add(
                User(
                    email=email,
                    password_hash=generate_password_hash(password),
                )
            )
            db.commit()
            return redirect(url_for("home.index"))


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "GET":
        return render_template("login.j2")
    elif request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            sa.select(User).where(User.email == email)
        ).scalar_one_or_none()

        if user is None:
            return render_template("login.j2")

        success = check_password_hash(user.password_hash, password)

        return str(success)
