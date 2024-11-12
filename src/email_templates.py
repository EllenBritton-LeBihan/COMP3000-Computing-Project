from faker import Faker
fake = Faker()

def generate_email(category):
    return {
        'subject': fake.sentence(),
        'sender': fake.email(),
        'recipient': fake.email(),
        'body': fake.text(),
        'category': category
    }

def family_friends_template():
    return {
        'subject': f"Hey! Just checking in {fake.first_name()}",
        'sender': fake.email(),
        'recipient': fake.email(),
        'body': f"Hey {fake.first_name()}, how have you been? Just wanted to {fake.sentence()}",
        'category': 'family_friends'
    }

def work_template():
    return {
        'subject': f"Project Update: {fake.word()}",
        'sender': fake.email(),
        'recipient': fake.email(),
        'body': f"Dear {fake.first_name()},\n\nPlease review the latest updates on {fake.sentence()}. Regards, {fake.name()}",
        'category': 'work'
    }

def phishing_template():
    return {
        'subject': f"Urgent: Action Required to Verify Account",
        'sender': fake.email(),
        'recipient': fake.email(),
        'body': f"Dear User, there is an issue with your account! Verify your details here: http://malicious-link.com\n\nThanks, {fake.company()} Support",
        'category': 'phishing'
    }