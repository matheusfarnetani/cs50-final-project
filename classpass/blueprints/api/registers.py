from ...database.models import Cards, Equipments, Places, Registers
from ...extensions import db


def getRegisters(argsCard = None, argsDate = None, argsTime = None, argsType = None, argsPlace = None) -> dict:

    query = db.session.query(
        Cards.type.label('card type'),
        Cards.uid.label('card uid'),
        Registers.date,
        Registers.hour,
        Registers.minute,
        Registers.second,
        Equipments.description.label('equipment'),
        Places.description.label('place')
    )

    # Joining tables with explicit join conditions
    query = query.join(Registers, Cards.id == Registers.card_id)
    query = query.join(Equipments, Registers.equipment_id == Equipments.id)
    query = query.join(Places, Equipments.place_id == Places.id)

    # Add conditions based on user input
    if argsCard:
        query = query.filter(Cards.uid.like(f"%{argsCard}%"))
    if argsDate:
        query = query.filter(Registers.date == argsDate)
    if argsTime:
        query = query.filter(
            Registers.hour == argsTime.hour,
            Registers.minute == argsTime.minute,
            Registers.second == argsTime.second
        )
    if argsType:
        query = query.filter(Cards.type == argsType)
    if argsPlace:
        query = query.filter(Places.description == argsPlace)

    # Add ORDER BY clause
    query = query.order_by(
        Registers.date.desc(),
        Registers.hour.desc(),
        Registers.minute.desc(),
        Registers.second.desc()
    )

    query = query.limit(50)

    # Execute the query and fetch the results as a list of dictionaries
    results = []
    for row in query.all():
        result_dict = {
            'card type': row[0].value,
            'card uid': row[1],
            'date': row[2].strftime('%d/%m/%Y'),
            'hour': str(row[3]),
            'minute': str(row[4]),
            'second': str(row[5]),
            'equipment': row[6],
            'place': row[7]
        }
        results.append(result_dict)

    return results
