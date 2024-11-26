from flask import Flask
from flask_mail import Mail, Message
import sqlite3


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

#mail to test routes work with mailhog 
@app.route("/test_email")
def test_email():
    try:
        msg = Message(
            subject="Test Email",
            sender="test@example.com",
            recipients=["recipient@example.com"],
            body="This is a test email."
        )
        mail.send(msg)
        return "Test email sent!"
    except Exception as e:
        print(f"Error: {e}")
        return f"Failed to send test email: {e}"
    
#func to select a random email from the db each time it's called
def get_random_email():
    try: 
        conn = sqlite3.connect("emails.db", check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("SELECT subject, sender, recipient, body, category FROM emails ORDER BY RANDOM() LIMIT 1")
        email = cursor.fetchone()
        print(f"Retrieved email: {email}")
        return email
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None 
    finally:
        conn.close()

#route to send a random email from the database using Flask-Mail
@app.route("/send_random_email")
def send_random_email():
    email = get_random_email()
    if email:
        # Strip unwanted newline characters or extra spaces from the values
        subject, sender, recipient, body, category = email
        subject = subject.strip()    # remove spaces and newlines
        sender = sender.strip()      # 
        recipient = recipient.strip() # 
        body = body.strip()          # 
        category = category.strip()  #

        print(f"Sending email from {sender} to {recipient} with subject {subject}")

        msg = Message(
            subject=subject,
            sender=sender,
            recipients=[recipient]
        )
        msg.body = body

        try:
            mail.send(msg)
            return f"Email sent to {recipient} with subject '{subject}'"
        except Exception as e:
            print(f"Error sending email: {e}")
            return f"Error sending email: {e}"
    else:
        return "No email found in database!"

# init db when the app starts
if __name__ == "__main__":
    app.run(debug=True)