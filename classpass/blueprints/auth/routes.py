from flask import Blueprint, render_template
from flask_login import login_required

# Blueprint Variable
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/")
@login_required
def index():
    return render_template("overview.html")