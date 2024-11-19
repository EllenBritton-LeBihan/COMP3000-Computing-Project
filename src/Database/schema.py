import sqlite3



def create_tables():
    conn = sqlite3.connect("Data/emails.db") 
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            sender TEXT,
            recipient TEXT,
            body TEXT,
            category TEXT,
            contains_suspicious_link BOOLEAN,
            mismatched_display_name BOOLEAN,
            urgent_language BOOLEAN,
            suspicious_attachment BOOLEAN
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()