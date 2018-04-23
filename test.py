from app.db import db

def testData(): # this makes bogus data
    c = db.get_db()
    for i in (0, 8):
        for j in (0, 8):
            command = "INSERT INTO BOARD (x, y, color, king) VALUES (" + str(i) + ", " + str(j) + ", None, 0);"
            c.execute(command)

c = db.get_db()
db.getBoardState()
testData()
fd = open("testdata.sql")
sqlit = fd.read().split(';')
for command in sqlit:
    c.execute(command)
    print("running command: " + command)

