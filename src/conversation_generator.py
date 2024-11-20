import sqlite3
import random
import os 

from db_utils import get_connection, execute_query
from email_templates import family_friends_template_labelled, work_template_labelled,  phishing_template_labelled
from schema import create_tables

def generate_conversation(conn, cursor, num_emails=50):
    for _ in range(num_emails):
        contact_type = random.choice(['family_friends', 'work', 'phishing'])
        if contact_type == 'family_friends':
            email = family_friends_template_labelled()
        elif contact_type == 'work':
            email = work_template_labelled()
        else:
            email = phishing_template_labelled()

#insert email and features into db
        cursor.execute('''
            INSERT INTO emails (subject, sender, recipient, body, category, contains_suspicious_link, 
                                mismatched_display_name, urgent_language, suspicious_attachment)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            email['subject'], 
            email['sender'], 
            email['recipient'], 
            email['body'], 
            email['category'], 
            email['features']['contains_suspicious_link'], 
            email['features']['mismatched_display_name'], 
            email['features']['urgent_language'], 
            email['features']['suspicious_attachment']
        ))
    conn.commit()

if __name__ == '__main__':
    conn = get_connection()  # uses db_utils for connection
    cursor = conn.cursor()
    create_tables()  # Ensures the table exists
    generate_conversation(conn, cursor, 50)
    conn.close()