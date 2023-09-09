# Populates Database

import random
from datetime import datetime, timedelta, date, time
from dateutil.relativedelta import relativedelta
from itertools import permutations, product


def main():
    cards = create_cards(char1="A", char2="B", group1=2, group2=5)
    number_of_cards = len(cards)
    people_per_group = number_of_cards / 9
    student_group = people_per_group * 6
    collaborator_group = people_per_group * 2
    places = create_places(number_of_places=15)
    equipments = create_equipments(number_of_places=len(places), eqp_per_place=5)
    arduinos = create_arduinos(total_equipments=len(equipments) * 5)
    courses = create_courses(number_of_courses=20)
    students = create_students(number_of_students=student_group, number_of_courses=len(courses))
    work_sectors = create_work_sectors(number_of_sectors=6)
    collaborators = create_collaborators(number_of_collaborators=collaborator_group, work_sectors=work_sectors, people_per_group=people_per_group)
    visitants = create_visitants(number_of_visitants=people_per_group)
    # registers = create_registers(len(cards), 5)


def create_arduinos(total_equipments: int) -> list:
    """Creates one arduino for each equipment."""
    arduinos = list()
    counter = 1
    while counter <= total_equipments:
        arduino = dict()
        arduino["description"] = f"Arduino {counter}"
        arduino["code_version"] = "0.0.1"
        arduinos.append(arduino)
        counter += 1

    return arduinos


def create_cards(char1: str, char2: str, group1: int, group2: int) -> list:
    """Generates all possibilities of strings;\n
        Strings format; 'AA AA AA AA AA';\n
        from 'A' to 'C'."""

    cards = list()

    # Create list of characters from A to C
    characters = [chr(i) for i in range(ord('A'), ord('C')+1)]

    # Create all combinations of the instance in list, in groups of 'repeat'
    combinations = list(product(characters, repeat=2))

    # Clean combinations
    clean_combinations = [''.join(combination) for combination in combinations]

    # Generate all possible strings in groups of 5 - "AA AA AA AA AA"
    combined_strings = list(product(clean_combinations, repeat=5))

    # Clean combinations
    result_strings = [' '.join(combined) for combined in combined_strings]

    number_of_cards = len(result_strings)
    # 59.049
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
        collaborator["work_sector"] = random.choice(work_sectors)
        if i < people_per_group:
            collaborator["work_shift_starts"] = time(hour=8, minute=0, second=0)
            collaborator["work_shift_ends"] = time(hour=17, minute=0, second=0)
        else:
            collaborator["work_shift_starts"] = time(hour=14, minute=0, second=0)
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


def create_equipments(number_of_places: int, eqp_per_place: int) -> list:
    """Create 'x' equipments per place."""
    equipments = list()
    counter2 = 0
    for i in range(number_of_places):
        index = i + 1
        for j in range(eqp_per_place):
            counter2 += 1
            equipment = dict()
            equipment["description"] = f"Equipment {counter2}"
            equipment["eqp_type"] = "walls"
            equipment["date_last_inspection"] = random_date(start_year=2023, end_year=2023)
            equipment["date_next_inspection"] = equipment["date_last_inspection"] + relativedelta(months=6)
            equipment["place_id"] = index
            equipments.append(equipment)

    return equipments


def create_places(number_of_places: int) -> list:
    """Create list with 'x' strings;\n
        Strings format: 'place 1'."""
    places = list()
    for i in range(number_of_places):
        places.append(f"place {i + 1}")

    return places


def create_registers(number_of_cards: int, registers_by_card: int) -> list:
    """Creates 'x' registers of 'y' cards"""
    registers = list()
    group_of_cards = number_of_cards / 9
    for i in range(number_of_cards):
        for j in range(registers_by_card):
            register = dict()
            register["date"] = random_date(2023, 2023)
            temp_time = random_time(start_hour=8, end_hour=23)


def create_students(number_of_students: int, number_of_courses: int) -> list:
    """Create 'x' students."""
    students = list()
    for i in range(number_of_students):
        student = dict()
        student["name"] = f"student {i + 1}"
        student["birthday"] = random_date(1980, 2005)
        student["course"] = random.randint(1, number_of_courses)
        student["course_start"] = date(random.randint(2019, 2023), 1, 1)
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
    random_year = random.randint(start_year, end_year)
    random_month = random.randint(1, 12)
    if random_month == 2:
        random_day = random.randint(1, 28)
    elif random_month in {4, 6, 9, 11}:
        random_day = random.randint(1, 30)
    else:
        random_day = random.randint(1, 31)
    
    return date(random_year, random_month, random_day)


def random_time(start_hour: int, end_hour: int) -> time:
    """Generate random time between hours."""
    random_hour = random.randint(start_hour, end_hour)
    random_minute = random.randint(0, 59)
    random_second = random.randint(0, 59)

    return time(random_hour, random_minute, random_second)


if __name__ == "__main__":
    main()