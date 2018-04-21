import sqlite3

from app.db import db

conn = sqlite3.connect('db.db')

# conn.execute("SELECT TABLES LIKE 'STATS")
# result = conn.fetchone()
# if not result:
#     init = open('init.sql', 'r')
#     fileText = init.read()
#     init.close()
#     sqlCommands = fileText.split(';')  
#     for command in sqlCommands:
#         conn.execute(command)

# for sqllite

init = open('app/db/initsqlite.sql', 'r')
fileText = init.read()
init.close()
sqlCommands = fileText.split(';')  
for command in sqlCommands:
    conn.execute(command)
    print("running command: " + command)