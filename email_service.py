import os
import resend
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")
USER = os.getenv("GMAIL_USER")

class EmailDeliveryError(Exception):
    """Raised when the email could not be delivered."""

def send_email(contact):
    try:
        resend.Emails.send(
            {
                "from": "Portfolio <onboarding@resend.dev>",
                "to": USER,
                "reply_to": contact.email,
                "subject": contact.subject,
                "text": f"""Nova mensagem do portfólio!

Nome: {contact.name}
Email: {contact.email}

Mensagem:
{contact.message}
""",
            }
        )
    except Exception as error:
        raise EmailDeliveryError from error