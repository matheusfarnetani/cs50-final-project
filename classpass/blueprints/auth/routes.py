from urllib.parse import quote

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from ...database.models import Cards

# Blueprint Variable
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
@login_required
def index():

    # Check if the user is logged in
    if not current_user.is_authenticated:
        return redirect(url_for("common.login", next=url_for("common.login")))

    # Display account info
    acc_info = dict()
    acc_info["username"] = current_user.username
    acc_info["email"] = current_user.email
    acc_info["type"] = current_user.type.value.title()
    acc_info["uid"]= Cards.query.filter_by(id=current_user.card_id).first().uid

    return render_template("overview.html", card_id=quote(acc_info["uid"]), acc_info=acc_info)