from flask import Blueprint, render_template, request, Response, g, url_for, redirect

from .auth import login_required
from .db import get_db
from .models import Newsletter


bp = Blueprint("newsletters", __name__, url_prefix="/newsletters")


@bp.route("/")
@login_required
def index():
    user = g.user

    newsletters = user.newsletters

    return render_template("newsletter.j2", newsletters=newsletters)


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "GET":
        return render_template("create_newsletter.j2")
    elif request.method == "POST":

        print(request.form)

        name = request.form["name"]

        db = get_db()

        newsletter = Newsletter(name=name)
        newsletter.users = [g.user]

        db.add(newsletter)
        db.commit()

        return redirect(url_for("newsletters.index"))
    else:
        return Response(status=405)
