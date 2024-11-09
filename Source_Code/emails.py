import sqlite3
from faker import Faker
import random

# init faker
fake = Faker()
# define into categories 
categories = ['regular', 'phishing', 'spam']

#connect to db
conn = sqlite3.connect('emails.db')
cursor = conn.cursor()

# table for emails (if not exists)
cursor.execute('''
CREATE TABLE IF NOT EXISTS emails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT,
    sender TEXT,
    recipient TEXT,
    body TEXT,
    category TEXT
)
''')

# func to create synthetic emails
def generate_email(category):
    return {
        'subject': fake.sentence(),
        'sender': fake.email(),
        'recipient': fake.email(),
        'body': fake.text(),
        'category': category
    }

# insert into db
for _ in range(100):  #range
    category = random.choice(categories)
    
    if category == 'phishing':
        # phishing email generation using indicators.
        email = generate_email(category)
        email['body'] = f"{email['body']} \n\n Urgent: Verify your account here: http://malicious-link.com"
    else:
        email = generate_email(category)

    cursor.execute('''
    INSERT INTO emails (subject, sender, recipient, body, category)
    VALUES (?, ?, ?, ?, ?)
    ''', (email['subject'], email['sender'], email['recipient'], email['body'], email['category']))
# commit and close
conn.commit()
conn.close()