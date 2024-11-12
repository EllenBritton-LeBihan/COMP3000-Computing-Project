import sqlite3
from faker import Faker
import random
from email_templates import generate_email, family_friends_template, work_template, phishing_template

fake = Faker()
categories = ['regular', 'phishing', 'spam']

def setup_database():
    conn = sqlite3.connect('emails.db')
    cursor = conn.cursor()
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
    conn.commit()
    return conn, cursor

def populate_basic_emails(conn, cursor, num_emails=100):
    for _ in range(num_emails):
        category = random.choice(categories)
        email = generate_email(category)
        if category == 'phishing':
            email['body'] += "\n\nUrgent: Verify your account here: http://malicious-link.com"
        cursor.execute('''
            INSERT INTO emails (subject, sender, recipient, body, category)
            VALUES (?, ?, ?, ?, ?)
        ''', (email['subject'], email['sender'], email['recipient'], email['body'], email['category']))
    conn.commit()

if __name__ == "__main__":
    conn, cursor = setup_database()
    populate_basic_emails(conn, cursor, 100)
    conn.close()