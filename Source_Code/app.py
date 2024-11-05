from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

# server config for MailHog
app.config["MAIL_SERVER"] = "localhost"  # server 
app.config["MAIL_PORT"] = 1025           # SMTP port
app.config["MAIL_USE_TLS"] = False       # no TLS needed for local testing with MailHog
app.config["MAIL_USE_SSL"] = False       # no SSL need for local testing with MailHog
app.config["MAIL_USERNAME"] = None       # no username needed for MailHog
app.config["MAIL_PASSWORD"] = None       # no pass needed for MailHog

mail = Mail(app)

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