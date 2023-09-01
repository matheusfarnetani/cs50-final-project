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
    rows = cur.execute("SELECT * FROM users WHERE username = ?;", (username,))

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
       Returns true if it is available."""

    rows = cur.execute(
        "SELECT username FROM users WHERE username = ?;", (username,))
    rows = cur.fetchall()

    if rows:
        return False

    return True


def validate_dictionary(input_dict):

    # Define the expected keys and their data types
    expected_keys = ['username', 'email', 'hash', 'type']
    expected_data_types = {
        expected_keys[0]: str,
        expected_keys[1]: str,
        expected_keys[2]: str,
        expected_keys[3]: str,
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

    if not validate_dictionary(user):
        return False

    # Execute the SQL insert statement
    cur.execute("INSERT INTO users (username, email, hash, user_type) VALUES (?, ?, ?, ?)",
                (user['username'], user['email'], user['hash'], user['type']))
    
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