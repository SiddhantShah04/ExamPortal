import sqlite3 as db

con2 = db.connect('Core JAVA.db')
cur2 = con2.cursor()
E = cur2.execute('select * from Paper')
R = E.fetchall()
print(R)