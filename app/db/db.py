from flask import jsonify
from string import Template
import json
import cx_Oracle

def getBoardState():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM BOARD") # get all the data from db
    entries = cursor.fetchall()
    if len(entries) == 0: # if there isn't any entries, give sample data
        new_game()
    jsonData = {}
    entityArray = []
    for entry in entries: # build json for every entity
        entityData = {}
        entityData['tile'] = entry[0]
        entityData['color'] = entry[1]
        if entry[2] == 0:
            entityData['king'] = False
        else:
            entityData['king'] = True
        entityArray.append(entityData) # add our built json to the array
    jsonData['tiles'] = entityArray
    return jsonData # return our built json

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
        cur.execute(command)
        con.commit()
