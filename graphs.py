import database.models as models
from app import create_app, db
from sqlalchemy import func


def people_by_type() -> dict:
    """Query the database and returns a dictionary with number of people by type.

    First key is 'labels' and it contains a list of labels.
    The following keys are listed in 'labels' and contains the data."""

    # Get total number of students
    number_of_students = db.session.query(models.Students).count()

    # Get total number of collaborators
    number_of_collaborators = db.session.query(models.Collaborators).count()

    # Get total number of visitants
    number_of_visitants = db.session.query(models.Visitants).count()

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
            models.Places.description.label('place_description'),
            func.count(models.Equipments.id).label('equipment_count')
        )
        .join(models.Equipments)
        .group_by(models.Places.description)
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
            models.Places.description.label('place_description'),
            func.count(models.Registers.id).label('register_count')
        )
        .join(models.Equipments, models.Registers.equipment_id == models.Equipments.id)
        .join(models.Places, models.Equipments.place_id == models.Places.id)
        .group_by(models.Places.description)
        .order_by(func.count(models.Registers.id).desc())
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
        db.session.query(models.Cards.type, func.count())
        .join(models.Registers, models.Registers.card_id == models.Cards.id)
        .join(models.Equipments, models.Equipments.id == models.Registers.equipment_id)
        .join(models.Places, models.Places.id == models.Equipments.place_id)
        .filter(models.Places.description == place)
        .group_by(models.Cards.type)
        .all()
    )

    result_places = db.session.query(models.Places.description).all()
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
