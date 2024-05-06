import sqlite3


def get_db_connection():
    conn = sqlite3.connect("BDPasserelle.db")
    conn.row_factory = sqlite3.Row
    return conn
