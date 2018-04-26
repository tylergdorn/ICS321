from app.db import db
import math
import json
import ast

def allValidEnds(startstr):
    """When given a starting pos returns a list of valid ending positions"""
    start = 0
    try:
        start = int(startstr)
    except ValueError:
        print("whoops, this happens because reasons")
        start = math.floor(float(startstr))
    boardState = db.getBoardState()
    print(boardState['tiles'][start])
    startColor = getPieceColor(start)
    king = boardState['tiles'][start]['king']
    row = math.floor(start / 4)
    column = start % 4 + 1 # whoops i don't feel like changing it everywhere where I use 1 or 4 to 0 or 3 ¯\_(ツ)_/¯
    res = list()

    # print('row: ' + str(row) + ' column: ' + str(column))
    # start of the big horrible logic I can't think of how to make any nicer
    if(startColor == 'Red' or king):
        # this generates a table for fun math
        table = [1, 1, 1]
        if getPieceColor(start + 3) != 'None':
            table[0] = 0
        if getPieceColor(start + 4) != 'None':
            table[1] = 0
        if getPieceColor(start + 5) != 'None':
            table[2] = 0
        if(row % 2 == 0 and column != 4):
            res.append(start + 4 * table[1])
            res.append(start + 5 * table[2])
        elif(row % 2 == 0 and column == 4):
            res.append(start + 4 * table[1])
        if(row % 2 == 1 and column != 1):
            res.append(start + 3 * table[0])
            res.append(start + 4 * table[1])
        elif(row % 2 == 1 and column == 1):
            res.append(start + 4 * table[1])
            
    if(startColor == 'Black' or king):
        # this generates a table for fun math
        table = [-1, -1, -1]
        if getPieceColor(start - 3) != 'None':
            table[0] = 0
        if getPieceColor(start - 4) != 'None':
            table[1] = 0
        if getPieceColor(start - 5) != 'None':
            table[2] = 0
        # print(table)

        if(row % 2 == 0 and column != 4):
            res.append(start + 3 * table[0])
            res.append(start + 4 * table[1])
        elif(row % 2 == 0 and column == 4):
            res.append(start + 4 * table[1])
        if(row % 2 == 1 and column != 1):
            res.append(start + 4 * table[1])
            res.append(start + 5 * table[2])
        elif(row % 2 == 1 and column == 1):
            res.append(start + 4 * table[1])
    resu = [item for item in res if item != start]
    return resu
    
def validHops(sstart):
    """Returns a list of valid ending places for hop moves"""
    start = int(sstart)
    king = getKing(start)
    sColor = getPieceColor(start)
    sRow = math.floor(start / 4)
    sCol = start % 4
    moves = []
    res = []
    if(sColor == 'Red' or king):
        if sRow <= 6:
            if sCol == 0:
                moves.append(colRowToId(sRow + 2, sCol + 1))
            elif sCol == 3:
                moves.append(colRowToId(sRow + 2, sCol + 1))
            else:
                moves.append(colRowToId(sRow + 2, sCol + 1))
                moves.append(colRowToId(sRow + 2, sCol - 1))
    if(sColor == 'Black' or king):
        if sRow >= 1:
            if sCol == 0:
                moves.append(colRowToId(sRow - 2, sCol + 1))
            elif sCol == 3:
                moves.append(colRowToId(sRow - 2, sCol + 1))
            else: 
                moves.append(colRowToId(sRow - 2, sCol + 1))
                moves.append(colRowToId(sRow - 2, sCol - 1))
    for tile in moves:
        if getPieceColor(tile) == 'None':
            res.append(tile)
    return res

def validMoves(sstart):
    """This is somewhat of a misnomer, but allValidEnds is not the function that outputs all possible moves, this is"""
    start = int(sstart)
    hops = validHops(start)
    steps = allValidEnds(start)
    res = hops[:]
    for tile in hops:
        mid = 0
        row = math.floor(tile / 4)
        if row % 2 == 0:
            mid = math.ceil((tile + start) / 2)
        else:
            mid = math.floor((tile + start) / 2)
        if mid in steps:
            res.remove(tile)
    return {
        'hops': res,
        'steps': steps
    }

def getPieceColor(tile):
    """If given the boardstate and the tile you inquire about, gives you the color"""
    jsons = db.getBoardState()
    return jsons['tiles'][int(tile)]['color']

def getKing(tile):
    """If given the boardstate and the tile you inquire about, gives you the king status"""
    jsons = db.getBoardState()
    return jsons['tiles'][int(tile)]['king'] == True

def colRowToId(row, column):
    """when given column and row returns id"""
    return (row * 4) + column