from flask import jsonify
import sqlite3

def getBoardState():
    conn = get_db()
    cursor = conn.execute("SELECT * FROM BOARD")
    entries = cursor.fetchall()
    for entry in entries:
        print(entry)
def get_db():
    return sqlite3.connect('db.db')
