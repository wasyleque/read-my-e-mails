import imaplib
import email
from email.header import decode_header
from email.policy import default
import requests
import pyttsx3
from bs4 import BeautifulSoup
import re

# IMAP settings
IMAP_SERVER = 'your_imap_server_name'
IMAP_PORT = 993 #imap port number
IMAP_USERNAME = 'your_email_address_or_login'  # replace with your email address
IMAP_PASSWORD = 'your_password'  # replace with your password

# Define your filters
DATE_SINCE = "01-Jun-2024"  # format: 'DD-MMM-YYYY'
DATE_BEFORE = "07-Jul-2024"  # format: 'DD-MMM-YYYY'
SENDER_DOMAINS = ["netia.pl", "inpost.pl", "paczkomaty.pl", "facebookmail.com", "paypal.pl"] #reads e-mails from senders only from those domains
KEYWORDS = ["faktura", "paczka", "kod odbioru", "payment", "billing"] #reads e-mails with those keywords even if sender unknown

# Function to extract domain from email address
def get_domain(email_address):
    return email_address.split('@')[-1]

# Function to analyze text using local AI server ... still to do
#def analyze_text(text):
#    url = "http://192.168.0.10:8080/analyze"  # replace with your server's URL
#    response = requests.post(url, json={'text': text})
#    return response.json()

# Function to read text aloud
def read_aloud(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to clean HTML content
def clean_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text(separator=' ', strip=True)

# Function to remove URLs from text
def remove_urls(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)

# Connect to the server
mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
mail.login(IMAP_USERNAME, IMAP_PASSWORD)

# Select the inbox folder
mail.select('inbox')

# Search for emails within the date range
status, messages = mail.search(None, f'(SINCE {DATE_SINCE} BEFORE {DATE_BEFORE})')

messages = [int(num) for num in messages[0].split()]
messages.sort(reverse=True)

last50_messages = messages[:50]
for num in last50_messages:
    status, msg_data = mail.fetch(str(num), '(RFC822)')
    raw_message = msg_data[0][1]

    # Parse the email
    message = email.message_from_bytes(raw_message, policy=default)

    # Decode the sender
    from_address = message['From']
    from_domain = get_domain(from_address)
    
    # Decode the subject
    subject_header = decode_header(message['Subject'])
    subject = ''
    for part, encoding in subject_header:
        if isinstance(part, bytes):
            encoding = encoding if encoding else 'utf-8'
            try:
                part = part.decode(encoding)
            except (LookupError, UnicodeDecodeError):
                part = part.decode('utf-8', errors='replace')
        subject += part

    # Extract the email body
    body = ''
    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get('Content-Disposition'))
            
            if 'attachment' not in content_disposition:
                if content_type == "text/plain":
                    body = part.get_payload(decode=True).decode(part.get_content_charset('utf-8'))
                    break  # prioritize plain text
                elif content_type == "text/html":
                    html_content = part.get_payload(decode=True).decode(part.get_content_charset('utf-8'))
                    body = clean_html(html_content)
    else:
        content_type = message.get_content_type()
        if content_type == "text/plain":
            body = message.get_payload(decode=True).decode(message.get_content_charset('utf-8'))
        elif content_type == "text/html":
            html_content = message.get_payload(decode=True).decode(message.get_content_charset('utf-8'))
            body = clean_html(html_content)

    # Remove URLs from the body
    body = remove_urls(body)

    # Check if the email matches the sender domain and keyword filters
    if any(domain in from_domain for domain in SENDER_DOMAINS) or any(keyword in subject for keyword in KEYWORDS):
        print('Od: ', from_address)
        print('Temat: ', subject)
        print('Treść: ', body)
        if 'Date' in message:
            print('Date: ', message['Date'])
        
        # Analyze the email content
        #analysis_result = analyze_text(body)
        #print('Analysis:', analysis_result)

        # Read the email content aloud
        read_aloud('Message from')
        read_aloud(from_address)
        read_aloud('Subject')
        read_aloud(subject)
        #read_aloud(body)

# Close the connection
mail.close()
mail.logout()
