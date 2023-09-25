from flask import Blueprint, render_template
from flask_login import current_user, login_required

# Blueprint Variable
graphs_bp = Blueprint("graphs", __name__, url_prefix="/graphs")


@graphs_bp.route("/")
# @login_required
def graph():

    return render_template("graphs.html")
