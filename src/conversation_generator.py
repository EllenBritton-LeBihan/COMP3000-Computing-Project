import sqlite3
import random
from email_templates import family_friends_template, work_template, phishing_template

def generate_conversation(conn, cursor, num_emails=50):
    for _ in range(num_emails):
        contact_type = random.choice(['family_friends', 'work', 'service_providers_phishing'])
        if contact_type == 'family_friends':
            email = family_friends_template()
        elif contact_type == 'work':
            email = work_template()
        else:
            email = phishing_template()

        cursor.execute('''
            INSERT INTO emails (subject, sender, recipient, body, category)
            VALUES (?, ?, ?, ?, ?)
        ''', (email['subject'], email['sender'], email['recipient'], email['body'], email['category']))
    conn.commit()

if __name__ == "__main__":
    conn = sqlite3.connect('emails.db')
    cursor = conn.cursor()
    generate_conversation(conn, cursor, 50)
    conn.close()