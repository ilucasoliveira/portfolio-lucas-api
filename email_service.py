import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("GMAIL_USER")
PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

def send_email(contact):
    msg = EmailMessage()
    msg["Subject"] = contact.subject
    msg["From"] = USER
    msg["To"] = USER
    msg["Reply-To"] = contact.email
    msg.set_content(
        f"""Nova mensagem do portfólio!

Nome: {contact.name}
Email: {contact.email}

Mensagem:
{contact.message}
"""
    )
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as server:
        server.login(USER, PASSWORD)
        server.send_message(msg)