import sqlite3

# Path to database
db = "./static/database/finance.db"

# Create connection to the database
con = sqlite3.connect(db, check_same_thread=False)


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


# Change sqlite3.row_factory to return dict
con.row_factory = dict_factory

# Create cursor to execute SQL statements
cur = con.cursor()


def query_username(username: str):
    """Query database for username"""
    rows = cur.execute("SELECT * FROM users WHERE username = ?;", (username,))
    rows = cur.fetchall()
    if len(rows) != 1:
        return None
    return rows[0]
