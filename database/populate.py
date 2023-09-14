from random import randint, choice
from datetime import datetime, timedelta, date, time
from dateutil.relativedelta import relativedelta
from itertools import product

import models

# Track number of equipments created by 'make_equipments()'
TRACK_EQUIPMENTS = 1


def main(db):

    # Create 'places' data
    places = create_places()

    db_places = list()
    for key, value in places.items():
        if isinstance(value, list):
            for item in value:
                db_places.append(models.Places(description=item[1]))
        else:
            db_places.append(models.Places(description=value[1]))

    # Create 'equipments' data
    equipments = make_equipments(places=places)

    db_equipments = list()
    for key, value in equipments.items():
       if isinstance(value, list):
            for item in value:
                equipment = models.Equipments(
                    description=item["description"],
                    eqp_type=item["eqp_type"],
                    date_last_inspection=item["date_last_inspection"],
                    date_next_inspection=item["date_next_inspection"],
                    place_id=item["place_id"])
                db_equipments.append(equipment)

    # Create 'arduinos' data
    global TRACK_EQUIPMENTS
    arduinos = create_arduinos(number_of_arduinos=TRACK_EQUIPMENTS - 1)

    db_arduinos = list()
    for item in arduinos:
        arduino = models.Arduinos(
            description=item["description"],
            code_version=item["code_version"],
            equipment_id=item["equipment_id"])
        db_arduinos.append(arduino)

    # Create 'cards' data
    cards = create_cards(char1="A", char2="C", group1=2, group2=4)

    db_cards = list()
    for item in cards:
        card = models.Cards(
            uid=item["uid"],
            type=item["type"]
        )
        db_cards.append(card)

    # Simple ratio
    # Students = 2/3
    # Collaborator = 2/9
    # Visitant = 1/9
    number_of_cards = len(cards)
    people_per_group = int(number_of_cards / 9)
    student_group = people_per_group * 6 
    collaborator_group = people_per_group * 2

    # Create student objective
    courses = create_courses(number_of_courses=10)

    # Create 'students' data
    students = create_students(
        number_of_students=student_group, courses=courses)

    db_students = list()
    for item in students:
        student = models.Students(
            name=item["name"],
            birthday=item["birthday"],
            course=item["course"],
            course_start=item["course_start"],
            card_id=item["card_id"]
        )
        db_students.append(student)
    
    # Create collaborator objective
    work_sectors = create_work_sectors(number_of_sectors=6)

    # Create 'collaborators' data
    collaborators = create_collaborators(
        number_of_collaborators=collaborator_group, work_sectors=work_sectors, people_per_group=people_per_group)

    db_collaborators = list()
    for item in collaborators:
        collaborator = models.Collaborators(
            name=item["name"],
            birthday=item["birthday"],
            work_sector=item["work_sector"],
            work_shift_starts=item["work_shift_starts"],
            work_shift_ends=item["work_shift_ends"],
            card_id=item["card_id"]
        )
        db_collaborators.append(collaborator)
    
    # Create 'visitants' data
    visitants = create_visitants(number_of_visitants=people_per_group)

    db_visitants = list()
    for item in visitants:
        visitant = models.Visitants(
            name=item["name"],
            birthday=item["birthday"],
            document=item["document"],
            card_id=item["card_id"]
        )
        db_visitants.append(visitant)

    # Create 'registers' data
    registers = make_registers(
        number_of_cards=number_of_cards, days=3, equipments=equipments)

    db_registers = list()
    for item in registers:
        register = models.Registers(
            date=item["date"],
            hour=item["hour"],
            minute=item["minute"],
            second=item["second"],
            card_id=item["card_id"],
            equipment_id=item["equipment_id"]
        )
        db_registers.append(register)
    
    # Add into database
    db.session.add_all(db_places)
    db.session.add_all(db_equipments)
    db.session.add_all(db_arduinos)
    db.session.add_all(db_cards)
    db.session.add_all(db_students)
    db.session.add_all(db_collaborators)
    db.session.add_all(db_visitants)
    db.session.add_all(db_registers)
    db.session.commit() 


def create_arduinos(number_of_arduinos: int) -> list:
    """Creates one arduino for each equipment."""
    arduinos = list()
    for i in range(number_of_arduinos):
        arduino = dict()
        arduino["description"] = f"Arduino {i + 1}"
        arduino["code_version"] = "0.0.1"
        arduino["equipment_id"] = i + 1
        arduinos.append(arduino)

    return arduinos


def create_cards(char1: str, char2: str, group1: int, group2: int) -> list:
    """Generates all possibilities of strings;\n
        Strings format; 'AA AA AA AA';\n
        from 'A' to 'C'."""

    cards = list()

    # Create list of characters from A to C
    characters = [chr(i) for i in range(ord(char1), ord(char2) + 1)]

    # Create all combinations of the instance in list, in groups of 'repeat'
    combinations = list(product(characters, repeat=group1))

    # Clean combinations
    clean_combinations = [''.join(combination) for combination in combinations]

    # Generate all possible strings in groups
    combined_strings = list(product(clean_combinations, repeat=group2))

    # Clean combinations
    result_strings = [' '.join(combined) for combined in combined_strings]

    number_of_cards = len(result_strings)  # 6561
    people_per_group = number_of_cards / 9
    number_of_students = people_per_group * 6
    number_of_collaborators = (people_per_group * 2) + number_of_students

    # Group combinations in 3 options
    for i in range(number_of_cards):
        if i < number_of_students:
            card_type = "student"
        elif i < number_of_collaborators:
            card_type = "collaborator"
        else:
            card_type = "visitant"

        card = dict()
        card["uid"] = result_strings[i]
        card["type"] = card_type
        cards.append(card)

    return cards


def create_collaborators(number_of_collaborators: int, work_sectors: list, people_per_group: int) -> list:
    """Create 'x' collaborators."""
    collaborators = list()
    card_id_start = people_per_group * 6
    for i in range(number_of_collaborators):
        collaborator = dict()
        collaborator["name"] = f"collaborator {i + 1}"
        collaborator["birthday"] = random_date(1960, 2000)
        collaborator["work_sector"] = choice(work_sectors)
        if i < people_per_group:
            collaborator["work_shift_starts"] = time(
                hour=8, minute=0, second=0)
            collaborator["work_shift_ends"] = time(hour=17, minute=0, second=0)
        else:
            collaborator["work_shift_starts"] = time(
                hour=14, minute=0, second=0)
            collaborator["work_shift_ends"] = time(hour=23, minute=0, second=0)

        collaborator["card_id"] = i + card_id_start
        collaborators.append(collaborator)

    return collaborators


def create_courses(number_of_courses: int) -> list:
    """Create 'x' courses"""
    courses = list()
    for i in range(number_of_courses):
        courses.append(f"course {i + 1}")

    return courses


def create_equipments(number_of_equipments: int, place_id: int, place_name: str) -> list:
    """Create 'x' equipments per place."""
    global TRACK_EQUIPMENTS
    temp_equipments = list()
    for i in range(number_of_equipments):
        equipment = dict()
        equipment["id"] = TRACK_EQUIPMENTS
        TRACK_EQUIPMENTS += 1
        equipment["description"] = f"{place_name} Equipment {i + 1}"
        equipment["eqp_type"] = "walls"
        equipment["date_last_inspection"] = random_date(
            start_year=2023, end_year=2023)
        equipment["date_next_inspection"] = equipment["date_last_inspection"] + \
            relativedelta(months=6)
        equipment["place_id"] = place_id
        temp_equipments.append(equipment)

    return temp_equipments


def make_equipments(places: dict) -> dict:
    equipments = dict()
    equipments["library"] = list()
    equipments["hovet"] = list()
    equipments["entrances"] = list()
    equipments["classes"] = list()
    equipments["work"] = list()

    for key, value in places.items():
        if key == "library":
            equipments["library"].extend(create_equipments(
                number_of_equipments=6, place_id=1, place_name=key))
        elif key == "hovet":
            equipments["hovet"].extend(create_equipments(
                number_of_equipments=3, place_id=2, place_name=key))
        elif key == "entrances":
            for item in value:
                equipments["entrances"].extend(create_equipments(
                    number_of_equipments=5, place_id=item[0], place_name=key))
        elif key == "classes":
            for item in value:
                equipments["classes"].extend(create_equipments(
                    number_of_equipments=1, place_id=item[0], place_name=key))
        elif key == "work":
            for item in value:
                equipments["work"].extend(create_equipments(
                    number_of_equipments=2, place_id=item[0], place_name=key))

    return equipments


def create_places() -> dict:
    """Create dict of places to guide other creations."""
    places = dict()
    places["library"] = (1, "library")
    places["hovet"] = (2, "hovet")
    places["entrances"] = list()
    places["classes"] = list()
    places["work"] = list()
    for i in range(15):
        if i < 3:
            places["entrances"].append((i + 3, f"entrance {i + 1}"))
        elif i < 13:
            places["classes"].append((i + 3, f"class {i - 2}"))
        else:
            places["work"].append((i + 3, f"work {i - 12}"))

    return places


def flatten_equipments(dict: dict):
    temp_list = list()

    for key, value in dict.items():
        if key == "entrances":
            continue
        elif isinstance(value, list):
            for item in value:
                temp_list.append(item["id"])

    return temp_list


def make_registers(number_of_cards: int, days: int, equipments: dict) -> list:
    """Creates 'x' registers of 'y' cards"""
    registers = list()

    group_of_cards = number_of_cards / 9
    number_of_students = group_of_cards * 6
    half_students = number_of_students / 2
    number_of_collaborators = (group_of_cards * 2) + number_of_students
    half_collaborators = group_of_cards + number_of_students
    half_visitants = number_of_collaborators + (group_of_cards / 2)

    # Create day object
    today = datetime.today()
    register_day = (today - timedelta(days=days)).date()

    # Helpers
    all_equipments = flatten_equipments(equipments)
    entrance_visitor = equipments["entrances"][0]["id"]

    for i in range(days):
        for j in range(number_of_cards):
            if j < number_of_students:
                if j < half_students:
                    # Half students (morning)
                    registers.extend(register_sm(
                        equipments, all_equipments, register_day, j + 1))
                else:
                    # Half students (nocturne)
                    registers.extend(register_sn(
                    equipments, all_equipments, register_day, j + 1))
            elif j < number_of_collaborators:
                if j < half_collaborators:
                    # Half collaborators (monrning)
                    registers.extend(register_cm(equipments, register_day, j + 1))
                else:
                    # Half collaborators (nocturne)
                    registers.extend(register_cn(equipments, register_day, j + 1))
            elif j < half_visitants:
                # Half visitant (morning)
                registers.extend(register_vm(
                    entrance=entrance_visitor, equipments=all_equipments, day=register_day, card_id=j + 1))
            else:
                # Half visitant (nocturne)
                registers.extend(register_vn(
                    entrance=entrance_visitor, equipments=all_equipments, day=register_day, card_id=j + 1))

        register_day = register_day + timedelta(days=1)

    return registers


def create_students(number_of_students: int, courses: list) -> list:
    """Create 'x' students."""
    students = list()
    for i in range(number_of_students):
        student = dict()
        student["name"] = f"student {i + 1}"
        student["birthday"] = random_date(1980, 2005)
        student["course"] = choice(courses)
        student["course_start"] = date(randint(2019, 2023), 1, 1)
        student["card_id"] = i + 1
        students.append(student)

    return students


def create_visitants(number_of_visitants: int) -> list:
    """Create 'x' visitants."""
    visitants = list()
    card_id_starts = number_of_visitants * 8
    for i in range(number_of_visitants):
        visitant = dict()
        visitant["name"] = f"visitant {i + 1}"
        visitant["birthday"] = random_date(1960, 2011)
        visitant["document"] = "valid document"
        visitant["card_id"] = i + card_id_starts
        visitants.append(visitant)

    return visitants


def create_work_sectors(number_of_sectors: int) -> list:
    """Creates 'x' sectors."""
    work_sectors = list()
    for i in range(number_of_sectors):
        work_sectors.append(f"sector {i + 1}")

    return work_sectors


def random_date(start_year: int, end_year: int) -> date:
    """Generate random birthday between years."""
    random_year = randint(start_year, end_year)
    random_month = randint(1, 12)
    if random_month == 2:
        random_day = randint(1, 28)
    elif random_month in {4, 6, 9, 11}:
        random_day = randint(1, 30)
    else:
        random_day = randint(1, 31)

    return date(random_year, random_month, random_day)


def register_sm(equipments: dict, all_equipments: list, day: date, card_id: int) -> list:
    temp_list = list()

    for i in range(4):
        register = dict()
        register["date"] = day
        register["card_id"] = card_id

        if i == 0:
            # First register
            register_time = time(8, randint(0, 59), randint(0, 59))
            register["equipment_id"] = choice(equipments["entrances"])["id"]
        elif i == 1:
            # Mid register
            register_time = time(hour=9, minute=0, second=0)
            register["equipment_id"] = choice(equipments["classes"])["id"]
        elif i == 2:
            # Random register
            register_time = time(10, randint(0, 59), randint(0, 59))
            register["equipment_id"] = choice(all_equipments)
        else:
            # Last register
            register_time = time(12, randint(0, 59), randint(0, 59))
            register["equipment_id"] = choice(equipments["entrances"])["id"]

        register["hour"] = register_time.hour
        register["minute"] = register_time.minute
        register["second"] = register_time.second

        temp_list.append(register)

    return temp_list


def register_sn(equipments: dict, all_equipments: list, day: date, card_id: int) -> list:
    temp_list = list()

    for i in range(4):
        register = dict()
        register["date"] = day
        register["card_id"] = card_id

        if i == 0:
            # First register
            register_time = time(19, randint(0, 59), randint(0, 59))
            register["equipment_id"] = choice(equipments["entrances"])["id"]
        elif i == 1:
            # Mid register
            register_time = time(hour=21, minute=0, second=0)
            register["equipment_id"] = choice(equipments["classes"])["id"]
        elif i == 2:
            # Random register
            register_time = time(10, randint(0, 59), randint(0, 59))
            register["equipment_id"] = choice(all_equipments)
        else:
            # Last register
            register_time = time(22, randint(0, 59), randint(0, 59))
            register["equipment_id"] = choice(equipments["entrances"])["id"]

        register["hour"] = register_time.hour
        register["minute"] = register_time.minute
        register["second"] = register_time.second

        temp_list.append(register)

    return temp_list


def register_cm(equipments: dict, day: date, card_id: int) -> list:
    temp_list = list()

    for i in range(3):
        register = dict()
        register["date"] = day
        register["card_id"] = card_id

        if i == 0:
            register_time = time(7, randint(30, 59), randint(0, 59))
            register["equipment_id"] = choice(equipments["entrances"])["id"]
        elif i == 1:
            register_time = time(8, 0, 0)
            register["equipment_id"] = choice(equipments["work"])["id"]
        else:
            register_time = time(17, randint(0, 30), randint(0, 59))
            register["equipment_id"] = choice(equipments["entrances"])["id"]

        register["hour"] = register_time.hour
        register["minute"] = register_time.minute
        register["second"] = register_time.second

        temp_list.append(register)

    return temp_list


def register_cn(equipments: dict, day: date, card_id: int) -> list:
    temp_list = list()

    for i in range(3):
        register = dict()
        register["date"] = day
        register["card_id"] = card_id

        if i == 0:
            register_time = time(13, randint(30, 59), randint(0, 59))
            register["equipment_id"] = choice(equipments["entrances"])["id"]
        elif i == 1:
            register_time = time(14, 0, 0)
            register["equipment_id"] = choice(equipments["work"])["id"]
        else:
            register_time = time(23, randint(0, 30), randint(0, 59))
            register["equipment_id"] = choice(equipments["entrances"])["id"]

        register["hour"] = register_time.hour
        register["minute"] = register_time.minute
        register["second"] = register_time.second

        temp_list.append(register)

    return temp_list


def register_vm(entrance: int, equipments: list, day: date, card_id: int) -> list:
    temp_list = list()

    for i in range(3):
        register = dict()
        register["date"] = day
        register["card_id"] = card_id

        if i == 0:
            register_time = time(9, randint(0, 30), randint(0, 59))
            register["equipment_id"] = entrance
        elif i == 1:
            register_time = time(9, randint(30, 59), randint(0, 59))
            register["equipment_id"] = choice(equipments)
        else:
            register_time = time(10, randint(0, 59), randint(0, 59))
            register["equipment_id"] = entrance

        register["hour"] = register_time.hour
        register["minute"] = register_time.minute
        register["second"] = register_time.second

        temp_list.append(register)

    return temp_list


def register_vn(entrance: int, equipments: list, day: date, card_id: int) -> list:
    temp_list = list()

    for i in range(3):
        register = dict()
        register["date"] = day
        register["card_id"] = card_id

        if i == 0:
            register_time = time(20, randint(0, 30), randint(0, 59))
            register["equipment_id"] = entrance
        elif i == 1:
            register_time = time(20, randint(30, 59), randint(0, 59))
            register["equipment_id"] = choice(equipments)
        else:
            register_time = time(21, randint(0, 59), randint(0, 59))
            register["equipment_id"] = entrance

        register["hour"] = register_time.hour
        register["minute"] = register_time.minute
        register["second"] = register_time.second

        temp_list.append(register)

    return temp_list


if __name__ == "__main__":
    main()
