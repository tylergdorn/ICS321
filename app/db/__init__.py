import sqlite3

from app.db import db
from app.db import gamelogic

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

# init = open('app/db/init.sql', 'r')
# fileText = init.read()
# init.close()
# sqlCommands = fileText.split(';') 
# conn = db.get_db() 
# cursor = conn.cursor()
# for command in sqlCommands:
#     cursor.execute(command)
#     print("running command: " + command)