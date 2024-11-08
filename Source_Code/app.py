from flask import Flask
from flask_mail import Mail, Message
import sqlite3
import random

app = Flask(__name__)

# server config for MailHog
app.config["MAIL_SERVER"] = "localhost"  # server 
app.config["MAIL_PORT"] = 1025           # SMTP port
app.config["MAIL_USE_TLS"] = False       # no TLS needed for local testing with MailHog
app.config["MAIL_USE_SSL"] = False       # no SSL need for local testing with MailHog
app.config["MAIL_USERNAME"] = None       # no username needed for MailHog
app.config["MAIL_PASSWORD"] = None       # no pass needed for MailHog

mail = Mail(app)

#func to select random email from db each time is called
def get_random_email():
    conn = sqlite3.connect('emails.db')
    cursor = conn.cursor()
    cursor.execute("SELECT subject, sender, recipient, body FROM emails ORDER BY RANDOM() LIMIT 1")
    email = cursor.fetchone()
    conn.close()
    return email

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

#setup route in Flask to fetch email from db to send thru Flask-Mail
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