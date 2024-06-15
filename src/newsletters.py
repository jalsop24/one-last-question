from flask import Blueprint, render_template, request, Response, g, url_for, redirect
from flask_mail import Message
import sqlalchemy as sa

from .auth import login_required
from .db import get_db
from .models import Newsletter, User
from .email import mail


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


@bp.route("/<int:id>/delete", methods=["DELETE"])
@login_required
def delete(id):

    db = get_db()

    newsletter = db.execute(
        sa.select(Newsletter).where(Newsletter.id == id)
    ).scalar_one_or_none()

    if newsletter is None:
        return Response(status=404)

    db.delete(newsletter)
    db.commit()

    return Response(status=200)


@bp.route("/<int:id>/send", methods=["POST"])
@login_required
def send(id: int):

    db = get_db()
    newsletter = db.execute(
        sa.select(Newsletter)
        .join(Newsletter.users)
        .where(User.id == g.user.id, Newsletter.id == id)
    ).scalar_one_or_none()

    if newsletter is None:
        return Response(status=404)

    message = Message(
        subject="test hello",
        sender=("Newsletter", "newsletters@one_last_question.io"),
        recipients=[user.email for user in newsletter.users],
    )

    message.html = render_template("email.j2", newsletter=newsletter)
    message.body = (
        f"I hope you like this newsletter. {newsletter.id = } {newsletter.name = }"
    )
    mail.send(message)

    return "sent"


@bp.route("/<int:id>/view")
def view(id: int):
    db = get_db()
    newsletter = db.execute(
        sa.select(Newsletter).where(Newsletter.id == id)
    ).scalar_one_or_none()
    if newsletter is None:
        return Response(status=404)

    return render_template("email.j2", newsletter=newsletter)
