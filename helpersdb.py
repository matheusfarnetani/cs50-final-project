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
    
    # Return first dict
    return rows[0]
