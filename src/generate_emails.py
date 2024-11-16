#populates and creates db emails

import sqlite3
import random
from email_templates import family_friends_template, work_template, phishing_template

def setup_database():
    conn = sqlite3.connect('emails.db') # persistent db
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

categories = ["family_friends", "work", "phishing"]

def populate_basic_emails(conn, cursor, num_emails=20):
    for _ in range(num_emails):
        category = random.choice(categories)

        if category == 'family_friends':
            print('Calling family_friends_template')
            email = family_friends_template()
        elif category == 'work':
            print('Calling work_template')
            email = work_template()
        elif category == 'phishing':
            print('Calling phishing_template')
            email = phishing_template()

        cursor.execute('''
            INSERT INTO emails (subject, sender, recipient, body, category)
            VALUES (?, ?, ?, ?, ?)
        ''', (email['subject'], email['sender'], email['recipient'], email['body'], email['category']))
    conn.commit()

if __name__ == '__main__':
    conn, cursor = setup_database()
    populate_basic_emails(conn, cursor, 20)
    conn.close()

    