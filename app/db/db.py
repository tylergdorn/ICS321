from flask import jsonify
from string import Template
import cx_Oracle

def getBoardState():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM BOARD")
    entries = cursor.fetchall()
    print(entries)
    if len(entries) == 0:
        new_game()
    for entry in entries:
        print(entry)
def get_db():
    file = open('server.txt')
    return cx_Oracle.connect(file.read())

def new_game():
    con = get_db()
    cur = con.cursor()
    for i in range(0, 32):
        template = Template('INSERT INTO BOARD VALUES (${i}, \'${color}\', 0)')
        color = 'Black'
        if i <= 20 and i > 12:
            color = 'None'
        elif i <= 20:
            color = 'Red'
        command = template.substitute(i = str(i), color = color)
        # print(command)
        cur.execute(command)
        con.commit()
