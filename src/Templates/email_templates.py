import random


import os 

pwd = os.getcwd()
print(pwd)

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
        f'Hey {recipient_name}, it’s been too long! We should chat soon.',
        f'What’s new, {recipient_name}? Let’s plan a family get-together soon.',
        f'Hi {recipient_name}, I was just thinking about you! Let’s catch up soon.'
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
        f'Hello {recipient_name}, I need you to check these updates ASAP.',
        f'Hey {recipient_name}, quick reminder to review the project details.',
        f'Hi {recipient_name}, please take a look at these changes for the project. Thanks!',
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


    #mismatched display names and email addresses
    spoofed_sender_email = random.choice([
        f'{sender_name.lower()}@secure-login.net',
        f'{sender_name.lower()}@support-verify.com',
        f'helpdesk@{random.choice(["accounts-security.com", "myupdates.live"])}'
    ])

    #variety of link styles
    malicious_link = random.choice([
        'http://192.168.0.1/verify',
        'http://bit.ly/secure-login',
        f'http://secure-login.{random.choice(["co", "io", "net"])}',
        f'https://{random.choice(["payppal", "rnicrosoft", "amazcn"])}-security-alert.com'
    ])

    #subject enhancement for phishing charecteristics
    subject_phishing_list = [
       'Verify Account Ownership Immediately',
        'Urgent: Account Security Breach Detected',
        'Immediate Action Required: Verify Payment Details',
        'Security Alert: Unusual Login Attempt',
        'Your Account is at Risk! Respond Now',
        'Action Required: Failed Payment Attempt Detected'
    ]
    subject = random.choice(subject_phishing_list)


    body_phishing_template = [
          f"Dear {recipient_name},\n\nWe’ve detected a login attempt from an unrecognized device. To secure your account, verify your identity immediately: {malicious_link}\n\nBest regards,\nAccount Security Team",
        f"Hi {recipient_name},\n\nYour payment for the recent purchase failed. Please update your payment details using this link: {malicious_link}.\n\nRegards,\nBilling Department",
        f"Hello {recipient_name},\n\nSuspicious activity has been detected in your account. For your security, click here to confirm your account details: {malicious_link}.\n\nThank you,\nSupport Team",
        f"Dear {recipient_name},\n\nYour account will be permanently locked if verification is not completed within 24 hours. Verify now: {malicious_link}\n\nThank you,\nCustomer Support",
        f"Attention {recipient_name},\n\nUnusual activity detected! For your protection, please validate your account here: {malicious_link}\n\nRegards,\nSecurity Team",
    ]

    #gen suspicious attachmente names
    suspicious_attachment = random.choice([
        'invoice.exe', 'security_update_v1.js', 'payment_info.scr', 'account_details.zip', 'login_info.bat'
    ])

    #include the email body with or w/o attachments
    if random.choice([True, False]):
        body_text = f"{random.choice(body_phishing_template)}\n\nAttachment: {suspicious_attachment}"
    else:
        body_text = random.choice(body_phishing_template)

    return {
        'subject': f"Subject: {subject}\n",
        'sender': f"Sender: {spoofed_sender_email}\n",
        'recipient': f"Recipient: {recipient_email}\n",
        'body': f"Email Body: {body_text}\n",
        'category': 'phishing'
    }

def family_friends_template_labelled():
    #generates a family/friends email with relevant flags.
    template = family_friends_template()
    return{
        **template,
        'features': {
            'contains_suspicious_link': False,
             'mismatched_display_name': False,
             'urgent_language': False,
             'suspicious_attachement': False,
        }
    }

def work_template_labelled():
    template = work_template()
    return {
        **template,
        'features': {
            'contains_suspicious_link': False,
            'mismatched_display_name': False,
            'ugrent_language': 'Urgent' in template['subject'],
            'suspicious_attachment': False,
        }
    }

def phishing_template_labelled():
    template = phishing_template()
    suspicious_flags = {
        'contains_suspicious_link': True,
        'mismatched_display_name': '@example' not in template['sender'],
        'urgenet_language': 'Urgent' in template['subject'] or 'Action Required' in template['subject'],
        'suspicious_attachment': 'Attachment:' in template['body']
    }
    return {**template, 'features': suspicious_flags}

