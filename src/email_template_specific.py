import sqlite3
import random


conn = sqlite3.connect('emails_simulation.db')
cursor = conn.cursor()

#create emails table for isolated convo flow
cursor.execute('''
CREATE TABLE IF NOT EXISTS emails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT,
    sender TEXT,
    receiver TEXT,
    content TEXT,
    compromised INTEGER
)
''')

#defing tone and layout
TONE_STYLES = {
    "casual": {"sign_off": "Cheers", "signature": "Lex", "spacing": "\n"},
    "formal": {"sign_off": "Thanks", "signature": "Lexi", "spacing": "\n\n"},
}

# trusted domains
TRUSTED_DOMAINS = ["example.com", "friendmail.com"]

#email content generation
def generate_email(subject, sender, receiver, tone="casual", compromised=False):
    style = TONE_STYLES[tone]
    sign_off = style["sign_off"]
    signature = style["signature"]
    spacing = style["spacing"]

    if compromised:
        # comprimised email with small dif
        content = (
            f"Hey {receiver.split('@')[0]},{spacing}"
            f"Cool sounds perfect.{spacing}"
            f"Also just to lyk I've started a website to sell my crochet! Here's the link: https://JennysCrochet.org{spacing}"
            f"{sign_off},\n{signature}"
        )
    else:
        #normal email with different styles
        content = (
            f"Hiya {receiver.split('@')[0]},{spacing}"
            f"Hope all is good! Just wondering if you're free on Tuesday to catch up?{spacing}"
            f"{sign_off},\n{signature}"
        )
    return content

# Simulating email convo
def simulate_conversation(conversation_id):
    # Randomize sender and receiver
    sender = f"Lexi@{random.choice(TRUSTED_DOMAINS)}"
    receiver = f"Jenny@{random.choice(TRUSTED_DOMAINS)}"
    subject = f"Conversation {conversation_id}: Let's catch up soon!"

    emails = []
    tone = random.choice(["casual", "formal"]) #random choice of tone for person

    for i in range(random.randint(4, 5)):  # 4 to 5 emails per conversation
        compromised = (i == 3)  # making every fourth email compromised
        email = {
            "subject": subject,
            "sender": sender if i % 2 == 0 else receiver,
            "receiver": receiver if i % 2 == 0 else sender,
            "content": generate_email(subject, sender, receiver, tone=tone, compromised=compromised),
            "compromised": int(compromised),
        }
        emails.append(email)

    return emails

#populate the db
def populate_database(num_conversations):
    for conv_id in range(1, num_conversations + 1):
        conversation = simulate_conversation(conv_id)
        for email in conversation:
            cursor.execute(
                '''
                INSERT INTO emails (subject, sender, receiver, content, compromised)
                VALUES (?, ?, ?, ?, ?)
                ''',
                (email["subject"], email["sender"], email["receiver"], email["content"], email["compromised"])
            )

#create 20 ex
populate_database(20)
conn.commit()
conn.close()