from app.db import db

def validMove(start, end):
    """Checks if a move is valid"""
    if start > 31 or start < 0 or end > 31 or end < 0: # impossible gamestates
        return False
    boardState = db.getBoardState()
    difference = abs(start - end)
    if difference != 4 or difference != 5 or difference != 7 or difference != 9:
        return False # these are the only differences that are legal move. multi-hop moves are considered non turn ending moves.
    if difference < 5: # i.e. a hop over another piece
        # if boardState.tiles[start]
        1 == 1