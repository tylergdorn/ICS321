from flask import jsonify
from string import Template
import json
import sqlite3
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
        new_game('')
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
    conn.commit()
    conn.close()
    return jsonData # return our built json

def get_db():
    """Returns a database connection"""
    return sqlite3.connect('db.db', timeout=1)

def new_game(team):
    """Starts a new game, and resets the db. Takes team that won"""
    con = get_db()
    cur = con.cursor()
    stats = getStats()
    clearGame()
    t = Template('UPDATE STATS SET ${team}WINS=${num}')
    if(team == 'Red'):
        wins = stats[0][0]
        cur.execute(t.substitute(team = 'RED', num = wins + 1))
    elif(team == 'Black'):
        wins = stats[0][1]
        cur.execute(t.substitute(team = 'BLACK', num = wins + 1))
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
    con.close()
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
                changeTurn()
                print("steppin!")
                movePiece(start, end)
                gl.shouldbeKing(end)

def movePiece(start, end):
    """moves a piece from start to end in the database"""
    print('this is being called')
    con = get_db()
    cur = con.cursor()
    startColor = gl.getPieceColor(start)
    endColor = gl.getPieceColor(end)
    startKing = gl.getKing(start)
    endKing = gl.getKing(end)
    sKing = 1 if startKing else 0
    eKing = 1 if endKing else 0 #these last four lines get the king status, and translate it to 1/0 since oracle doesn't like true/false
    t = Template("UPDATE BOARD SET color='${color}', king=${king} WHERE tile=${tile}")
    cur.execute(t.substitute(tile = start, color = endColor, king = eKing))
    cur.execute(t.substitute(tile = end, color = startColor, king = sKing))
    con.commit()
    con.close()

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
    con.commit()
    movePiece(start, end)
    # TODO: MAKE THIS CHECK IF YOU CAN JUMP MORE, THEN CHANGE TURN
    con.close()
    gl.shouldbeKing(end)
    gl.isOver()
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
    con.close()

def clearGame():
    """Clears everything out of the board table"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM BOARD")
    conn.commit()
    conn.close()
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
    conn.close()

def kingPiece(tile):
    """Makes piece at tile a king"""
    con = get_db()
    cur = con.cursor()
    t = Template("UPDATE BOARD SET king=1 WHERE tile=${tile}")
    print('kinged')
    cur.execute(t.substitute(tile=tile))
    con.commit()
    con.close()