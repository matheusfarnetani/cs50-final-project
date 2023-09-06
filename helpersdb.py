import sqlite3

# Path to database
db = "./static/database/data.db"

# Create connection to the database
con = sqlite3.connect(db, check_same_thread=False)


# Change sqlite3 return type, from list of tuples to list of dicts
def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


# Change sqlite3.row_factory to return dict
con.row_factory = dict_factory

# Create cursor to execute SQL statements
cur = con.cursor()


def query_username(username: str) -> dict:
    """Query database for username, and get all results;\n
    Returns None if result is diferent than 1;\n
    Returns dict, with corresponded user's data, if result is 1."""
    rows = cur.execute(
        "SELECT * FROM users WHERE username = (?);", (username,))

    # Select all from query
    rows = cur.fetchall()

    # If it is different than 1.
    # There are multiple users with same username or there is none.
    # Both were considered errors.
    if len(rows) != 1:
        return None
    return rows[0]


def check_username(username: str) -> bool:
    """Query database for username;\n
       Returns True if it is available."""

    rows = cur.execute(
        "SELECT username FROM users WHERE username = (?);", (username,))
    rows = cur.fetchall()
    if rows:
        return False
    return True


def check_card_uid(cardUid: str, cardType: str) -> bool:
    """Query database for card UID;\n
       Returns True if it exists"""

    rows = cur.execute(
        "SELECT * FROM cards WHERE type = (?) AND uid = (?);", (cardType, cardUid))
    rows = cur.fetchall()
    if rows:
        return True
    return False


def get_cardId(cardUid: str, cardType: str) -> int:
    """Query database for card id;\n
       Returns ID if card UID exist;\n
       Returns -1 if card UID doesn't exist."""

    rows = cur.execute(
        "SELECT id FROM cards WHERE type = (?) AND uid = (?);", (cardType, cardUid))
    rows = cur.fetchall()
    if rows and len(rows) == 1:
        return rows[0]['id']
    return -1


def validate_dictionary(input_dict: dict) -> bool:

    # Define the expected keys and their data types
    expected_keys = ['username', 'email', 'hash', 'type', 'card']
    expected_data_types = {
        expected_keys[0]: str,
        expected_keys[1]: str,
        expected_keys[2]: str,
        expected_keys[3]: str,
        expected_keys[4]: str,
    }

    # Check if all expected keys are present in the dictionary
    for key in expected_keys:
        if key not in input_dict:
            return False

    # Check if the data types of values match the expected types
    for key, expected_type in expected_data_types.items():
        if key in input_dict and not isinstance(input_dict[key], expected_type):
            return False

    # All checks passed; the dictionary has the expected structure
    return True


def create_new_user(user: dict) -> bool:
    """Create new user in database"""

    # Check dict structure
    if not validate_dictionary(user):
        return False

    # Get card's id
    card_id = get_cardId(user['card'], user['type'])
    if card_id == -1:
        return False

    # Execute the SQL insert statement
    cur.execute("INSERT INTO users (username, email, hash, user_type, card_id) VALUES (?, ?, ?, ?, ?)",
                (user['username'], user['email'], user['hash'], user['type'], user['card']))

    # Commit the transaction
    con.commit()

    return True


def get_by_username(username: str) -> dict:
    """Returns, as dict, all data from user"""

    rows = cur.execute("SELECT * FROM users WHERE username = (?)", (username,))
    rows = cur.fetchall()
    if rows and len(rows) == 1:
        return rows[0]
    return None


def get_locals():
    """Get locals for displaying"""

    rows = cur.execute("SELECT * FROM locals;")
    rows = cur.fetchall()
    if rows:
        return rows
    return False


def search_tables(card=None, date=None, time=None, card_type=None, local=None):
    """Get data for displaying"""

    # Base SQL query without WHERE clauses
    sql_query = """
    SELECT cards.type AS 'card type',
        cards.uid AS 'card uid',
        registers.date,
        registers.hours,
        registers.minutes,
        registers.seconds,
        equipments.description AS equipment,
        locals.name AS local
    FROM register_has_card
        JOIN cards ON register_has_card.card_id = cards.id
        JOIN registers ON register_has_card.register_id = registers.id
        JOIN register_has_equipment ON register_has_equipment.register_id = registers.id
        JOIN equipments ON equipments.id = register_has_equipment.equipment_id
        JOIN locals ON locals.id = equipments.local_id
    """

    # Add conditions based on user input
    conditions = []
    if card:
        conditions.append(f"cards.uid LIKE '%{card}%'")
    if date:
        conditions.append(f"registers.date = '{date}'")
    if time:
        conditions.append(f"registers.hours = '{time.hour}'")
        conditions.append(f"registers.minutes = '{time.minute}'")
        conditions.append(f"registers.seconds = '{time.second}'")
    if card_type:
        conditions.append(f"cards.type = '{card_type}'")
    if local:
        conditions.append(f"locals.name = '{local}'")


    # Add WHERE clause if conditions exist
    if conditions:
        sql_query += "WHERE " + " AND ".join(conditions)

    # Add ORDER BY clause
    sql_query += "ORDER BY date DESC, hours DESC, minutes DESC, seconds DESC"

    # Execute the SQL query
    cur.execute(sql_query)

    # Fetch the results
    results = cur.fetchall()

    return results
