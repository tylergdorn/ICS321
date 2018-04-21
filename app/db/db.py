from flask import jsonify
import sqlite3

conn = sqlite3.connect('db.db')

def getBoardState():
    cursor = conn.execute("SELECT * FROM ")
