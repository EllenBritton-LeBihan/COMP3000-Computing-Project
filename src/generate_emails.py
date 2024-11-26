#populates and creates db emails

import sqlite3
import random
from email_templates import family_friends_template_labelled, work_template_labelled, phishing_template_labelled, spam_template_labelled
from db_utils import get_connection, execute_query
from schema import create_tables


categories = ["family_friends", "work", "phishing", "spam"]

def populate_emails(conn, cursor, num_emails=20):
    for _ in range(num_emails):
        category = random.choice(categories)

        if category == 'family_friends':
            email = family_friends_template_labelled()
        elif category == 'work':
            email = work_template_labelled()
        elif category == 'spam':
            email = spam_template_labelled()
        elif category == 'phishing':
            email = phishing_template_labelled()
        

        cursor.execute('''
            INSERT INTO emails (subject, sender, recipient, body, category, 
                       
                                contains_suspicious_link, mismatched_display_name, 
                                urgent_language, suspicious_attachment)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            email['subject'], email['sender'], email['recipient'], email['body'], email['category'],
            email['features']['contains_suspicious_link'],
            email['features']['mismatched_display_name'],
            email['features']['urgent_language'],
            email['features']['suspicious_attachment'],
        ))
    conn.commit()

if __name__ == '__main__':
    conn = get_connection()
    cursor = conn.cursor()
    create_tables()
    populate_emails(conn, cursor, 20)
    conn.close()

    