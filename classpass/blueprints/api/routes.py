from flask import Blueprint, request, jsonify
from flask_login import login_required

from ...extensions import login_manager
from ...database.models import Users
from .graphs import people_by_type, equipments_by_place, registers_by_place, place_user
from .registers import getRegisters

# Blueprint Variable
api_bp = Blueprint("api", __name__, url_prefix="/api")


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Routes
@api_bp.route("/graphs/<int:graph_id>")
# @login_required
def data_graphs(graph_id):
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
# @login_required
def data_table():
    
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
