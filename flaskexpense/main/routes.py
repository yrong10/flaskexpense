from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("expenses.dashboard"))
    return render_template("index.html")


@main.route("/about")
@login_required
def about():
    return render_template("dashboard/about.html")
