import sqlite3

#This is just a script to create the database
conn = sqlite3.connect('./static/CSCDemo.db')

conn.commit()
conn.close()
