from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from ...database.models import Places
from .forms import SearchTable

# Blueprint Variable
tables_bp = Blueprint("tables", __name__, url_prefix="/tables")

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