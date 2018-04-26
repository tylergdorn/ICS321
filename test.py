import math

def validMoves(start):
    """This is somewhat of a misnomer, but allValidEnds is not the function that outputs all possible moves, this is"""
    hops = [18, 16]
    steps = [13, 14]
    print(hops)
    print(steps)
    res = hops[:]
    for tile in hops:
        print(tile)
        mid = 0
        row = math.floor(tile / 4)
        if row % 2 == 0:
            mid = math.ceil((tile + start) / 2)
        else:
            mid = math.floor((tile + start) / 2)
        print(mid)
        print(mid in steps)
        if mid in steps:
            res.remove(tile)
            print(res)
        print(hops)
        print(tile)
    print('ended')
    return {
        'hops': hops,
        'steps': steps
    }

validMoves(9)