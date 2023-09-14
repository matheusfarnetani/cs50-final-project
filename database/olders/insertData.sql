-- Insert data in order to make the app work as expected
-- Cards data
INSERT INTO cards (type, uid)
VALUES ("student", "AA AA AA AA");
INSERT INTO cards (type, uid)
VALUES ("student", "AA AA BB BB");
INSERT INTO cards (type, uid)
VALUES ("student", "AA AA CC CC");
INSERT INTO cards (type, uid)
VALUES ("collaborator", "BB BB AA AA");
INSERT INTO cards (type, uid)
VALUES ("collaborator", "BB BB BB BB");
INSERT INTO cards (type, uid)
VALUES ("collaborator", "BB BB CC CC");
INSERT INTO cards (type, uid)
VALUES ("visitor", "CC CC AA AA");
INSERT INTO cards (type, uid)
VALUES ("visitor", "CC CC BB BB");
INSERT INTO cards (type, uid)
VALUES ("visitor", "CC CC CC CC");
-- Local data
INSERT INTO locals (name)
VALUES ("local 01");
INSERT INTO locals (name)
VALUES ("local 02");
INSERT INTO locals (name)
VALUES ("local 03");
-- Equipment data
INSERT INTO equipments (
        description,
        type,
        date_last_inspection,
        local_id
    )
VALUES ("equip. 01", "ticket gate", "2023-09-02", 1);
INSERT INTO equipments (
        description,
        type,
        date_last_inspection,
        local_id
    )
VALUES ("equip. 02", "ticket gate", "2023-09-02", 2);
INSERT INTO equipments (
        description,
        type,
        date_last_inspection,
        local_id
    )
VALUES ("equip. 03", "ticket gate", "2023-09-02", 3);
-- Arduino data
INSERT INTO arduinos (
        description,
        code_version,
        date_last_update,
        equipment_id
    )
VALUES ("arduino 01", "0.0.01", "2023-09-02", 1);
INSERT INTO arduinos (
        description,
        code_version,
        date_last_update,
        equipment_id
    )
VALUES ("arduino 02", "0.0.01", "2023-09-02", 2);
INSERT INTO arduinos (
        description,
        code_version,
        date_last_update,
        equipment_id
    )
VALUES ("arduino 03", "0.0.01", "2023-09-02", 3);
-- Registers data
-- Register 1
INSERT INTO registers (date, hours, minutes, seconds)
VALUES ("2023-09-02", 19, 20, 32);
INSERT INTO register_has_equipment (register_id, equipment_id)
VALUES (1, 1);
INSERT INTO register_has_card (register_id, card_id)
VALUES (1, 1);
-- Register 2
INSERT INTO registers (date, hours, minutes, seconds)
VALUES ("2023-09-02", 19, 20, 50);
INSERT INTO register_has_equipment (register_id, equipment_id)
VALUES (2, 2);
INSERT INTO register_has_card (register_id, card_id)
VALUES (2, 2);
-- Register 3
INSERT INTO registers (date, hours, minutes, seconds)
VALUES ("2023-09-02", 19, 21, 30);
INSERT INTO register_has_equipment (register_id, equipment_id)
VALUES (3, 1);
INSERT INTO register_has_card (register_id, card_id)
VALUES (3, 3);
-- Register 4
INSERT INTO registers (date, hours, minutes, seconds)
VALUES ("2023-09-02", 19, 22, 12);
INSERT INTO register_has_equipment (register_id, equipment_id)
VALUES (4, 3);
INSERT INTO register_has_card (register_id, card_id)
VALUES (4, 4);
-- Register 5
INSERT INTO registers (date, hours, minutes, seconds)
VALUES ("2023-09-02", 19, 23, 20);
INSERT INTO register_has_equipment (register_id, equipment_id)
VALUES (5, 2);
INSERT INTO register_has_card (register_id, card_id)
VALUES (5, 5);
-- Register 6
INSERT INTO registers (date, hours, minutes, seconds)
VALUES ("2023-09-02", 19, 24, 20);
INSERT INTO register_has_equipment (register_id, equipment_id)
VALUES (6, 3);
INSERT INTO register_has_card (register_id, card_id)
VALUES (6, 6);
-- Register 7
INSERT INTO registers (date, hours, minutes, seconds)
VALUES ("2023-09-02", 19, 24, 20);
INSERT INTO register_has_equipment (register_id, equipment_id)
VALUES (7, 1);
INSERT INTO register_has_card (register_id, card_id)
VALUES (7, 7);
-- Register 8
INSERT INTO registers (date, hours, minutes, seconds)
VALUES ("2023-09-02", 19, 26, 37);
INSERT INTO register_has_equipment (register_id, equipment_id)
VALUES (8, 1);
INSERT INTO register_has_card (register_id, card_id)
VALUES (8, 8);
-- Register 9
INSERT INTO registers (date, hours, minutes, seconds)
VALUES ("2023-09-02", 19, 27, 10);
INSERT INTO register_has_equipment (register_id, equipment_id)
VALUES (9, 1);
INSERT INTO register_has_card (register_id, card_id)
VALUES (9, 9);