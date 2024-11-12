from flask import Flask
from flask_mail import Mail, Message
import sqlite3
import random
from generate_emails import setup_database, populate_basic_emails
from conversation_generator import generate_conversation

# init flask app
app = Flask(__name__)

#config MailHog server
app.config["MAIL_SERVER"] = "localhost"  # MH server
app.config["MAIL_PORT"] = 1025           # MHSMTP port
app.config["MAIL_USE_TLS"] = False       # TLS off for local testing
app.config["MAIL_USE_SSL"] = False       # SSL off for local testing
app.config["MAIL_USERNAME"] = None       # No user required for MH
app.config["MAIL_PASSWORD"] = None       # No pass needed for MH

mail = Mail(app)

#func to init db and populate it with emails
def initialize_database():
    conn, cursor = setup_database()
    populate_basic_emails(conn, cursor, 100)  # generate 100 basic emails
    generate_conversation(conn, cursor, 50)   # generate 50 convo emails
    conn.close()

#func to select a random email from the db each time it's called
def get_random_email():
    conn = sqlite3.connect('emails.db')
    cursor = conn.cursor()
    cursor.execute("SELECT subject, sender, recipient, body FROM emails ORDER BY RANDOM() LIMIT 1")
    email = cursor.fetchone()
    conn.close()
    return email

#flask route to send a basic test email using Flask-Mail
@app.route("/send_email")
def send_email():
    msg = Message(
        "Hello from Flask-Mail",
        sender="sender@example.com",
        recipients=["recipient@example.com"]
    )
    msg.body = "This is a test email sent from a Flask application"
    msg.html = "<h1>This is an HTML version of the email</h1>"
    mail.send(msg)
    return "Email sent!"

# route to send a random email from the database using Flask-Mail
@app.route("/send_random_email")
def send_random_email():
    email = get_random_email()
    if email:
        subject, sender, recipient, body = email
        msg = Message(
            subject=subject,
            sender=sender,
            recipients=[recipient]
        )
        msg.body = body
        mail.send(msg)
        return f"Email sent to {recipient} with subject '{subject}'"
    else:
        return "No email found in database!"

# init db when the app starts
if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)