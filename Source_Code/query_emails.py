import sqlite3

# connect to db
conn = sqlite3.connect('emails.db')
cursor = conn.cursor()

# just select reg
cursor.execute("SELECT * FROM emails WHERE category = 'regular'")
regular_emails = cursor.fetchall()

for email in regular_emails:
    print(email)

#close connection
conn.close()