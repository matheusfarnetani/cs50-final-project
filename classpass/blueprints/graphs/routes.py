from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

# Blueprint Variable
graphs_bp = Blueprint("graphs", __name__, url_prefix="/graphs")


@graphs_bp.route("/")
@login_required
def graph():

    # Check if the user is logged in
    if not current_user.is_authenticated:
        return redirect(url_for("common.login", next=url_for("common.login")))

    # Chart.js
    return render_template("graphs.html")
