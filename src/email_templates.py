import random

# Hardcoding for now; faker was causing issues
email_list = [
    'sarah.jameson@example.com',
    'michael.brown77@fakemail.net',
    'emma.greenfield@dummyemail.org',
    'lucas.richards92@tempmail.com',
]
first_name = [
    'Dan',
    'Sophie',
    'Mya',
    'Elizabeth',
    'Toby'
]

selected_first_name = random.choice(first_name)
selected_email_list = random.choice(email_list)

def family_friends_template():
    body_family_template = [
        f'Hi {selected_first_name}, how have you been? Let’s catch up soon!',
        f'Hello {selected_first_name}, just wanted to say hello!',
    ]
    return {
        'subject': f'Hey {selected_first_name}!',
        'sender': f'sender: {selected_email_list}',
        'recipient': f'recipient: {selected_email_list}',
        'body': random.choice(body_family_template),  
        'category': 'family_friends'
    }

def work_template():
    body_work_template = [
        f'Dear {selected_first_name}, please review the required updates on the project. Regards, {selected_first_name}',
        f'Hi {selected_first_name}, here are the key updates on the mentioned project.',
    ]
    return {
        'subject': "Project Update",
        'sender': selected_email_list,
        'recipient': selected_email_list,
        'body': random.choice(body_work_template), 
        'category': 'work'
    }

def phishing_template():
    body_phishing_template = [
        f'Dear User, there is an issue with your account! Verify your details here: http://malicious-link.com\nThanks for your Support\n',
    ]
    return {
        'subject': 'Urgent: Action Required to Verify Account',
        'sender': selected_email_list,
        'recipient': selected_email_list,
        'body': random.choice(body_phishing_template),  
        'category': 'phishing'
    }