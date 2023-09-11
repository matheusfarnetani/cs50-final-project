from random import randint, choice
from datetime import time, date


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
