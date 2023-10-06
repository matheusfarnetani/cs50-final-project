from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from ...database.models import Places
from .forms import SearchTable

# Blueprint Variable
tables_bp = Blueprint("tables", __name__, url_prefix="/tables")


@tables_bp.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Routes
@tables_bp.route('/')
@login_required
def tables():

    # Check if the user is logged in
    if not current_user.is_authenticated:
        return redirect(url_for("common.login", next=url_for("common.login")))

    # Create WTForm
    form = SearchTable(request.form)

    # Get all places
    places = Places.query.all()

    return render_template('tables.html', form=form, places=places)