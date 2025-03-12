#archived test was for first iterations of project, no longer relevant -- to be deleted.
import sqlite3

conn = sqlite3.connect('emails.db')
cursor = conn.cursor()

# check if emails table exists
cursor.execute("PRAGMA table_info(emails);")
columns = cursor.fetchall()
conn.close()

#print table structure
for column in columns:
    print(f"Column Name: {column[1]}, Data Type: {column[2]}")