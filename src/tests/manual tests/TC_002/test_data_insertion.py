#archived test was for first iterations of project, no longer relevant.
import sqlite3


#for generate_emails
print("Verifying email insertion\n")
conn = sqlite3.connect('emails.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM emails LIMIT 5;\n\n")
rows = cursor.fetchall()
conn.close()

for row in rows:
    print(row)
print("END\n")

#for conversation_generator
print("conversation type count for conversation_generator\n")
conn = sqlite3.connect('emails.db')
cursor = conn.cursor()

#count each category type to see if they were inserted
cursor.execute("SELECT category, COUNT(*) FROM emails GROUP BY category;")
category_counts = cursor.fetchall()
conn.close()

for category, count in category_counts:
    print(f"{category}: {count} emails\n\n")    


#manually inspecting simple data.
conn = sqlite3.connect('emails.db')
cursor = conn.cursor()
print("END\n")

#   Retrieve a few emails to inspect manually
print("Manually inspecting simple data\n")
cursor.execute("SELECT subject, sender, recipient, body, category FROM emails ORDER BY RANDOM() LIMIT 5;")
sample_emails = cursor.fetchall()
conn.close()

for email in sample_emails:
    subject, sender, recipient, body, category = email
    print("Subject:", subject)
    print("Sender:", sender)
    print("Recipient:", recipient)
    print("Body:", body)
    print("Category:", category)
    print("\n---\n")
print("END\n")