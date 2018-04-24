from flask import jsonify
from string import Template
import json
import cx_Oracle

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

def validMove(start, end):
    """Checks if a move is valid"""
    if start > 31 or start < 0 or end > 31 or end < 0: # impossible gamestates
        return False
    boardState = getBoardState()
    difference = abs(start - end)
    if difference != 4 or difference != 5 or difference != 7 or difference != 9:
        return False # these are the only differences that are legal move. multi-hop moves are considered non turn ending moves.
    if difference < 5: # i.e. a hop over another piece
        # if boardState.tiles[start]

def updatePosition(start, end):
    """Moves a piece from start to end"""
    con = get_db()
    cur = con.cursor()
    t = Template("SELECT * FROM BOARD WHERE tile=${tile}")
    cur.execute(t.substitute(tile = start))
    temp = cur.fetchall()
    startTile = temp[0]
    cur.execute(t.substitute(tile = end))
    temp2 = cur.fetchall()
    endTile = temp2[0]
    print(startTile)
    print(endTile)
    if startTile[1] != 'None':
        if endTile[1] == 'None':
            print('gj')


def clearGame():
    """Clears everything out of the board table"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM BOARD")
    conn.commit()
    print("Deleted All tile info from Board")

