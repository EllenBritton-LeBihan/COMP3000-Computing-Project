import sqlite3
import os



def get_connection(db_path=None):
    if db_path is None:
        db_path = os.path.join("..", "data", "emails.db")
    return sqlite3.connect(db_path)

def execute_query(conn, query, params=()):
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()