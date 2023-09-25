from flask import Blueprint, render_template, request

from ...database.models import Places
from .forms import SearchTable

# Blueprint Variable
tables_bp = Blueprint("tables", __name__, url_prefix="/tables")

@tables_bp.route('/')
# @login_required
def tables():

    # Create WTForm
    form = SearchTable(request.form)

    # Get all places
    places = Places.query.all()

    return render_template('tables.html', form=form, places=places)