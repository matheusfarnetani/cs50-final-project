from flask import Flask, flash, redirect, render_template, request, session, url_for, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from .database.models import Users, Cards
from .forms import Register_form, Login_form, SearchTable
from .extensions import login_manager, bcrypt, db

default_bp = Blueprint("data", __name__)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@default_bp.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@default_bp.route("/")
@login_required
def overview():
    # TODO - Display users info
    return render_template("overview.html")



