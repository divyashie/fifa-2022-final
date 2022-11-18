import sqlite3 

#Create a SQL Connection to our SQLite database 
conn = sqlite3.connect('test.db')
cur = conn.cursor()

for row in cur.execute("SELECT * FROM test"): 
    print(row)

conn.close()