from flask import jsonify
from string import Template
import json
import cx_Oracle
from app.db import gamelogic as gl
import math
import json
def getBoardState():
    """Returns the state of the board as json"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM BOARD ORDER BY tile") # get all the data from db
    entries = cursor.fetchall()
    if len(entries) == 0: # if there isn't any entries, give sample data
        new_game()
        return getBoardState()
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
    """Returns a database connection"""
    file = open('server.txt')
    return cx_Oracle.connect(file.read())

def new_game():
    """Starts a new game, and resets the db"""
    con = get_db()
    cur = con.cursor()
    # cur.execute("UPDATE ")
    for i in range(0, 32):
        template = Template('INSERT INTO BOARD VALUES (${i}, \'${color}\', 0)')
        color = 'Black'
        if i < 20 and i >= 12:
            color = 'None'
        elif i <= 12:
            color = 'Red'
        command = template.substitute(i = str(i), color = color)
        cur.execute(command)
        con.commit()
    print("Started New Game")

def getStats():
    """Returns all the stats of the current game as json"""
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM STATS")
    temp = cur.fetchall()
    return temp

def updatePosition(strstart, strend):
    """Moves a piece from start to end"""
    start = int(strstart)
    end = int(strend)
    valid = gl.validMoves(start)
    print(valid)
    combined = valid['hops'][:]
    combined.extend(valid['steps'])
    if end not in combined:
        return False
    startColor = gl.getPieceColor(start)
    endColor = gl.getPieceColor(end)
    print(valid)
    if startColor != 'None':
        if endColor == 'None':
            if end in valid['hops']:
                jump(start, end)
                print("hopping from " + str(start) + " to " + str(end))
            else:
                con = get_db()
                changeTurn()
                print("steppin!")
                cur = con.cursor()
                t = Template("UPDATE BOARD SET color='${color}' WHERE tile=${tile}")
                cur.execute(t.substitute(tile = start, color = endColor))
                cur.execute(t.substitute(tile = end, color = startColor))
                con.commit()

def jump(start, end):
    """executes a hop over one piece"""
    con = get_db()
    cur = con.cursor()
    sRow = math.floor(start / 4)
    print(sRow)
    # this works if you look at a board, trust me
    if(sRow % 2 == 0): # even row
        midId = math.ceil((start + end) / 2)
    if(sRow % 2 == 1): # odd row
        midId = math.floor((start + end) / 2)
    print(midId)
    t = Template("UPDATE BOARD SET color='${co}' WHERE tile=${ti}")
    cur.execute(t.substitute(co = 'None', ti = midId))
    cur.execute(t.substitute(co = gl.getPieceColor(start), ti = end))
    cur.execute(t.substitute(co = 'None', ti = start))
    # TODO: MAKE THIS CHECK IF YOU CAN JUMP MORE, THEN CHANGE TURN
    con.commit()
    changeTurn()

def changeTurn():
    """swaps the turn"""
    con = get_db()
    cur = con.cursor()
    startColor = cur.execute("SELECT turn FROM STATS").fetchall()[0][0]
    if(startColor == 'Red'):
        newcolor = 'Black'
    elif(startColor == 'Black'):
        newcolor = 'Red'
    t = Template("UPDATE STATS SET turn='${newColor}' WHERE turn='${startColor}'")
    cur.execute(t.substitute(newColor = newcolor, startColor = startColor))
    con.commit()

def clearGame():
    """Clears everything out of the board table"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM BOARD")
    conn.commit()
    print("Deleted All tile info from Board")

def init():
    """Initializes the db"""
    conn = get_db()
    cur = conn.cursor()
    f = open('app/db/init.sql', 'r')
    text = f.read()
    f.close()
    commands = text.split(';')
    for command in commands:
        if command != '': #this is because it thinks there is another command after the last ';'
            cur.execute(command) 
    conn.commit()