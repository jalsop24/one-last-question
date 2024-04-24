from flask import Blueprint, render_template

from .auth import login_required

bp = Blueprint("newsletters", __name__, url_prefix="/newsletters")


@bp.route("/")
@login_required
def index():
    return render_template("newsletter.j2")


@bp.route("/create")
@login_required
def create():
    return render_template("create_newsletter.j2")
