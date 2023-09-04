-- table users
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    hash TEXT NOT NULL,
    user_type TEXT CHECK(
        user_type IN ('student', 'collaborator', 'visitor')
    ) card_id INTEGER NOT NULL,
    FOREIGN KEY (card_id) REFERENCES cards(id)
);
CREATE UNIQUE INDEX username ON users (username);
-- Table registers
CREATE TABLE IF NOT EXISTS registers (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    date DATE NOT NULL,
    hour INTEGER NOT NULL,
    minute INTEGER NOT NULL,
    seconds INTEGER NOT NULL
);
-- Table errors
CREATE TABLE IF NOT EXISTS errors (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    date DATE NOT NULL,
    hour INTEGER NOT NULL,
    minute INTEGER NOT NULL,
    seconds INTEGER NOT NULL
);
-- Table cards
CREATE TABLE IF NOT EXISTS cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    type TEXT CHECK(type IN ('student', 'collaborator', 'visitor')) NOT NULL,
    serial CHAR(10) NOT NULL
);
-- Table students
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    birthday DATE NOT NULL,
    reg_number CHAR(8) NOT NULL,
    course TEXT NOT NULL,
    year_beginned YEAR NOT NULL,
    year_finshed YEAR NOT NULL,
    period TEXT CHECK(period IN ('morning', 'afternoon', 'nocturnal')) NOT NULL,
    card_id INTEGER NOT NULL,
    FOREIGN KEY (card_id) REFERENCES cards(id)
);
-- Table collaborators
CREATE TABLE IF NOT EXISTS collaborators (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    birthday DATE NOT NULL,
    reg_number CHAR(8) NOT NULL,
    sector TEXT NOT NULL,
    role TEXT NOT NULL,
    work_shift_start TIME NOT NULL,
    work_shift_end TIME NOT NULL,
    card_id INTEGER NOT NULL NOT NULL,
    FOREIGN KEY (card_id) REFERENCES cards(id)
);
-- Table 'visitants'
CREATE TABLE IF NOT EXISTS visitants (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    birthday DATE NOT NULL,
    document_type CHAR(5) NOT NULL,
    document CHAR(15) NOT NULL
);
-- Table 'telephones'
CREATE TABLE IF NOT EXISTS telephones (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    ddi CHAR(3),
    ddd CHAR(2) NOT NULL,
    number CHAR(9) NOT NULL,
    visitant_id INTEGER NOT NULL,
    FOREIGN KEY (visitant_id) REFERENCES visitants(id)
);
-- Table 'address'
CREATE TABLE IF NOT EXISTS addresses (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    type CHAR(10) NOT NULL,
    street VARCHAR(60) NOT NULL,
    number CHAR(10) NOT NULL,
    complement VARCHAR(15),
    city VARCHAR(60) NOT NULL,
    state VARCHAR(45) NOT NULL,
    zip_code VARCHAR(15) NOT NULL,
    visitant_id INTEGER NOT NULL,
    FOREIGN KEY (visitant_id) REFERENCES visitants(id)
);
-- Table 'locals'
CREATE TABLE IF NOT EXISTS locals (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(25)
);
-- Table 'equipments'
CREATE TABLE IF NOT EXISTS equipments (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    description VARCHAR(60),
    type VARCHAR(20) NOT NULL,
    date_last_inspection DATE NOT NULL,
    date_next_inspection DATE,
    local_id INTEGER NOT NULL,
    FOREIGN KEY (local_id) REFERENCES locals(id)
);
-- Table 'arduinos'
CREATE TABLE IF NOT EXISTS arduinos (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    description VARCHAR(60),
    code_version CHAR(6) NOT NULL,
    date_last_update DATE NOT NULL,
    equipment_id INTEGER NOT NULL,
    FOREIGN KEY (equipment_id) REFERENCES equipments(id)
);
-- Table 'register_has_equipment'
CREATE TABLE IF NOT EXISTS register_has_equipment (
    register_id INTEGER NOT NULL,
    equipment_id INTEGER NOT NULL,
    PRIMARY KEY (register_id, equipment_id),
    FOREIGN KEY (register_id) REFERENCES registers(id),
    FOREIGN KEY (equipment_id) REFERENCES equipments(id)
);
-- Table 'error_has_equipment'
CREATE TABLE IF NOT EXISTS error_has_equipment (
    error_id INTEGER NOT NULL,
    equipment_id INTEGER NOT NULL,
    PRIMARY KEY (error_id, equipment_id),
    FOREIGN KEY (error_id) REFERENCES errors(id),
    FOREIGN KEY (equipment_id) REFERENCES equipments(id)
);
-- Table 'register_has_card'
CREATE TABLE IF NOT EXISTS register_has_card (
    register_id INTEGER NOT NULL,
    card_id INTEGER NOT NULL,
    PRIMARY KEY (register_id, card_id),
    FOREIGN KEY (register_id) REFERENCES registers(id),
    FOREIGN KEY (card_id) REFERENCES cards(id)
);
-- Table 'error_has_card'
CREATE TABLE IF NOT EXISTS error_has_card (
    error_id INTEGER NOT NULL,
    card_id INTEGER NOT NULL,
    PRIMARY KEY (error_id, card_id),
    FOREIGN KEY (error_id) REFERENCES errors(id),
    FOREIGN KEY (card_id) REFERENCES cards(id)
);
-- Table 'visitant_has_card'
CREATE TABLE IF NOT EXISTS visitant_has_card (
    visitant_id INTEGER NOT NULL,
    card_id INTEGER NOT NULL,
    PRIMARY KEY (visitant_id, card_id),
    FOREIGN KEY (visitant_id) REFERENCES visitants(id),
    FOREIGN KEY (card_id) REFERENCES cards(id)
);
-- Create triggers
CREATE TRIGGER IF NOT EXISTS equipment_BEFORE_INSERT BEFORE
INSERT ON equipment FOR EACH ROW BEGIN
SET NEW.date_next_inspection = DATE(NEW.date_last_inspection, '+6 months');
END;