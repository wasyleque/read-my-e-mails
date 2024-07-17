import imaplib
import email
from email.header import decode_header
from email.policy import default
import requests
import pyttsx3
from bs4 import BeautifulSoup
import re

# IMAP settings
IMAP_SERVER = 'your_imap_server'
IMAP_PORT = 993 #imap port number
IMAP_USERNAME = 'your_mail_username'  # replace with your email address
IMAP_PASSWORD = 'your_password'  # replace with your password

# Define your filters
DATE_SINCE = "01-Jun-2024"  # format: 'DD-MMM-YYYY'
DATE_BEFORE = "16-Jul-2024"  # format: 'DD-MMM-YYYY'
SENDER_DOMAINS = ["netia.pl", "inpost.pl", "paczkomaty.pl", "facebookmail.com", "paypal.pl"] #reads e-mails from senders only from those domains
KEYWORDS = ["faktura", "paczka", "kod odbioru", "payment", "billing"] #reads e-mails with those keywords even if sender unknown

# Function to extract domain from email address
def get_domain(email_address):
    return email_address.split('@')[-1]

# Function to read text aloud
def read_aloud(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to clean HTML content
def clean_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return str(soup.get_text())

# Function to summarize text using Fabric
def summarize_text(text):
    with open('temp.txt', 'w') as f:
        f.write(text)
    
    command = ['fabric', 'text_summarizer:']
    summary_output = subprocess.check_output(command, shell=True).decode('utf-8')
    return summary_output.strip()

# Rest of your code...

print('Treść: ', body)
if 'Date' in message:
    print('Date: ', message['Date'])

# Summarize the email content
summary = summarize_text(body)
print('Summary:', summary)

# Read the email content aloud
read_aloud('Message from')
read_aloud(from_address)
read_aloud('Subject')
read_aloud(subject)
#read_aloud(body)

# Close the connection
mail.close()
mail.logout()
