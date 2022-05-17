import sqlite3

conn = sqlite3.connect('mydb.db')
cursor = conn.cursor()

cursor.execute("""CREATE TABLE """)