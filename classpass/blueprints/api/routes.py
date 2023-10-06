from flask import Blueprint, request, jsonify, redirect, url_for
from flask_login import login_required, current_user

from .graphs import people_by_type, equipments_by_place, registers_by_place, place_user
from .registers import getRegisters

# Blueprint Variable
api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Routes
@api_bp.route("/graphs/<int:graph_id>")
@login_required
def data_graphs(graph_id):

    # Check if the user is logged in
    if not current_user.is_authenticated:
        return redirect(url_for("common.login", next=url_for("common.login")))

    if graph_id == 1:
        data = people_by_type()
    elif graph_id == 2:
        data = equipments_by_place()
    elif graph_id == 3:
        data = registers_by_place()
    elif graph_id == 4:
        argsPlace = request.args.get("place")
        if not argsPlace:
            argsPlace = "entrance 01"
        data = place_user(argsPlace)
    else:
        return jsonify(None)

    return jsonify(data)


@api_bp.route('/tables')
@login_required
def data_table():

    # Check if the user is logged in
    if not current_user.is_authenticated:
        return redirect(url_for("common.login", next=url_for("common.login")))

    # Initialize route_args dictionary
    route_args = dict()

    # Mapping of parameters
    param_map = {
        'card': 'argsCard',
        'date': 'argsDate',
        'time': 'argsTime',
        'type': 'argsType',
        'place': 'argsPlace',
    }

    # Iterate through request parameters and map them to function arguments
    for param, arg_name in param_map.items():
        value = request.args.get(param)
        if value is not None:
            route_args[arg_name] = value

    results = getRegisters(**route_args)

    return jsonify(results)
