from ...database.models import Cards, Collaborators, Equipments, Places, Registers, Students, Visitants
from ...extensions import db
from sqlalchemy import func


def people_by_type() -> dict:
    """Query the database and returns a dictionary with number of people by type.

    First key is 'labels' and it contains a list of labels.
    The following keys are listed in 'labels' and contains the data."""

    # Get total number of students
    number_of_students = db.session.query(Students).count()

    # Get total number of collaborators
    number_of_collaborators = db.session.query(Collaborators).count()

    # Get total number of visitants
    number_of_visitants = db.session.query(Visitants).count()

    # Create data dict
    data = dict()
    data["labels"] = ["students", "collaborators", "visitants"]
    data["type"] = "bar"
    data["title"] = "Number of people by Card Type"
    data["students"] = number_of_students
    data["collaborators"] = number_of_collaborators
    data["visitants"] = number_of_visitants

    return data


def equipments_by_place() -> dict:
    """Query the database and returns a dictionary with number of equipments by place.

    First key is 'labels' and it contains a list of labels.
    The following keys are listed in 'labels' and contains the data."""

    # Join 'places' and 'equipments'
    result = (
        db.session.query(
            Places.description.label('place_description'),
            func.count(Equipments.id).label('equipment_count')
        )
        .join(Equipments)
        .group_by(Places.description)
        .all()
    )

    # Create data dict
    data = dict()
    data["type"] = "bar"
    data["labels"] = list()
    data["title"] = "Number of Equipments by Place"
    for instance in result:
        data["labels"].append(instance[0])
        data[instance[0]] = instance[1]

    return data


def registers_by_place() -> dict:
    """Query the database and returns a dictionary with number of registers by place.

    First key is 'labels' and it contains a list of labels.
    The following keys are listed in 'labels' and contains the data."""

    # Join 'places', 'equipments' and 'registers'
    result = (
        db.session.query(
            Places.description.label('place_description'),
            func.count(Registers.id).label('register_count')
        )
        .join(Equipments, Registers.equipment_id == Equipments.id)
        .join(Places, Equipments.place_id == Places.id)
        .group_by(Places.description)
        .order_by(func.count(Registers.id).desc())
        .all()
    )

    # Create data dict
    data = dict()
    data["type"] = "bar"
    data["labels"] = list()
    data["title"] = "Number of Registers by Place"
    for instance in result:
        data["labels"].append(instance[0])
        data[instance[0]] = instance[1]

    return data


def place_user(place: str) -> dict:
    """Query the database and returns a dictionary with total number of registers by type in place.

    First key is 'labels' and it contains a list of labels.
    The following keys are listed in 'labels' and contains the data."""

    result = (
        db.session.query(Cards.type, func.count())
        .join(Registers, Registers.card_id == Cards.id)
        .join(Equipments, Equipments.id == Registers.equipment_id)
        .join(Places, Places.id == Equipments.place_id)
        .filter(Places.description == place)
        .group_by(Cards.type)
        .all()
    )

    result_places = db.session.query(Places.description).all()
    places = [result_place[0] for result_place in result_places]

    # Create data dict
    data = dict()
    data["type"] = "bar"
    data["labels"] = list()
    data["title"] = f"Number of Registers by Type in {place.title()}"
    data["options"] = places
    for instance in result:
        data["labels"].append(instance[0].value)
        data[instance[0].value] = instance[1]

    return data
