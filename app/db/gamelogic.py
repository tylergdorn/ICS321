from app.db import db
import math

def validMove(start, end):
    """Checks if a move is valid"""
    if start > 31 or start < 0 or end > 31 or end < 0: # impossible gamestates
        return False


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
    startColor = getPieceColor(start, boardState)
    king = boardState['tiles'][start]['king']
    row = math.floor(start / 4)
    column = start % 4 + 1 # whoops i don't feel like changing it everywhere where I use 1 or 4 to 0 or 3 ¯\_(ツ)_/¯
    res = list()
    if(startColor == 'Red' or king):
        table = [1, 1, 1]
        if getPieceColor(start + 3, boardState) != 'None':
            table[0] = 0
        if getPieceColor(start + 4, boardState) != 'None':
            table[1] = 0
        if getPieceColor(start + 5, boardState) != 'None':
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
        table = [-1, -1, -1]
        if getPieceColor(start - 3, boardState) != 'None':
            table[0] = 0
        if getPieceColor(start - 4, boardState) != 'None':
            table[1] = 0
        if getPieceColor(start - 5, boardState) != 'None':
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
    resu = [item for item in res if item != start]
    return resu
    
def getPieceColor(tile, json):
    """If given the boardstate and the tile you inquire about, gives you the color"""
    return json['tiles'][tile]['color']