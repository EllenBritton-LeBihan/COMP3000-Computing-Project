import random

email_list = [
    'sarah.jameson@example.com',
'michael.brown77@fakemail.net',
    'emma.greenfield@dummyemail.org',
    'lucas.richards92@tempmail.com',
    'john.doe@example.com', 
    'emily.smith@example.net', 
    'chris.jones@example.org', 
    'sophia.lee@fakemail.com', 
    'james.miller@example.com', 
    'ava.taylor@dummyemail.org', 
    'michael.anderson@tempmail.com', 
    'isabella.clark@fakemail.net', 
    'william.davis@example.com', 
    'mia.martin@fakemail.org', 
    'alexander.garcia@tempmail.com', 
    'charlotte.evans@fakemail.net', 
    'ethan.moore@example.com', 
    'amelia.jackson@dummyemail.org', 
    'jacob.white@fakemail.net',
    'harper.harris@example.com', 
    'matthew.martinez@tempmail.com', 
    'evelyn.lopez@example.net'
]

sender_first_name = [
   'Sarah','Michael','Emma','Lucas','John', 'Emily','Chris','Sophia','James','Ava','Michael','Isabella','William','Mia','Alexander','Charlotte','Ethan','Amelia','Jacob','Harper','Matthew','Evelyn'
]

recipient_first_name = [
   'Sarah','Michael','Emma','Lucas','John', 'Emily','Chris','Sophia','James','Ava','Michael','Isabella','William','Mia','Alexander','Charlotte','Ethan','Amelia','Jacob','Harper','Matthew','Evelyn'
]

subject_family_list = [
    'Family Reunion: Let’s Catch Up Soon!',
    'Long Time No See! Let’s Reconnect',
    'Birthday Invitation: Come Celebrate with Us!',
    'Catch Up Soon? It’s Been Too Long!',
    'Family Gathering: Save the Date!',
    'How Have You Been? Let’s Plan a Get-Together!',
    'Miss You! Let’s Catch Up Soon!'
]

subject_work_list = [
    'Meeting Reminder: Project Update Discussion',
    'Upcoming Deadline: Submit Your Report ASAP',
    'New Task Assigned: Please Review by End of Day',
    'Team Meeting Agenda: Please Prepare Your Updates',
    'Project Progress Review: Urgent Feedback Needed',
    'Reminder: Final Report Due Tomorrow',
    'Client Call Update: Review the Notes Before Friday'
]

subject_phishing_list =  [
    'Urgent: Account Suspended - Immediate Action Required',
    'Critical Security Alert: Confirm Your Details Now',
    'Action Required: Your Account May Be Compromised',
    'Important: Your Account Has Been Locked',
    'Security Update: Immediate Verification Needed',
    'Suspicious Activity: Your Account Needs Verification',
    'Account Verification Alert: Immediate Action Required'
]

#email - to - name mapping for senders/recipients
sender_email_name_map = dict(zip(email_list, sender_first_name))
recipient_email_name_map = dict(zip(email_list, recipient_first_name))


def family_friends_template():
     
    sender_email = random.choice(email_list)
    recipient_email = random.choice(email_list)
    # make sure sender and recipient r different.
    while sender_email == recipient_email:
        recipient_email = random.choice(email_list)


    sender_name = sender_email_name_map[sender_email]
    recipient_name = recipient_email_name_map[recipient_email]

    #generating subject/body
    subject = random.choice(subject_family_list)
    body_family_template = [
        f'Hi {recipient_name}, how have you been? Let’s catch up soon!',
        f'Hello {recipient_name}, just wanted to say hello!',

    ]
    return {
        'subject': f"Subject: {subject}\n",
        'sender': f"Sender: {sender_email}\n",
        'recipient': f"Recipient: {recipient_email}\n",
        'body': f"Email Body: {random.choice(body_family_template)}\n",  
        'category': 'family_friends'
    }

def work_template():

    sender_email = random.choice(email_list)
    recipient_email = random.choice(email_list)
   
    while sender_email == recipient_email:
        recipient_email = random.choice(email_list)

    sender_name = sender_email_name_map[sender_email]
    recipient_name = recipient_email_name_map[recipient_email]

    subject = random.choice(subject_work_list)
    body_work_template = [
        f'Dear {recipient_name}, please review the required updates on the project. Regards, {sender_name}',
        f'Hi {recipient_name}, here are the key updates on the mentioned project.',
    ]
    return {
        'subject': f"Subject: {subject}\n",
        'sender': f"Sender: {sender_email}\n",
        'recipient': f"Recipient: {recipient_email}\n",
        'body': f"Email Body: {random.choice(body_work_template)}\n",  
        'category': 'work'
    }

def phishing_template():

    sender_email = random.choice(email_list)
    recipient_email = random.choice(email_list)
   
    while sender_email == recipient_email:
        recipient_email = random.choice(email_list)

    sender_name = sender_email_name_map[sender_email]
    recipient_name = recipient_email_name_map[recipient_email]

    subject = random.choice(subject_phishing_list)
    body_phishing_template = [
        f'Dear {recipient_name}, there is an issue with your account! Verify your details here: http://malicious-link.com\nThanks for your Support\n',
    ]
    return {
        'subject': f"Subject: {subject}\n",
        'sender': f"Sender: {sender_email}\n",
        'recipient': f"Recipient: {recipient_email}\n",
        'body': f"Email Body: {random.choice(body_phishing_template)}\n",   
        'category': 'phishing'
    }