import logging
import os

import resend
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

resend.api_key = os.getenv("RESEND_API_KEY")
USER = os.getenv("GMAIL_USER")
SENDER = os.getenv("RESEND_FROM", "Portfolio <onboarding@resend.dev>")


class EmailDeliveryError(Exception):
    """Raised when the email could not be delivered."""


def send_email(contact):
    try:
        resend.Emails.send(
            {
                "from": SENDER,
                "to": USER,
                "reply_to": contact.email,
                "subject": f"[Portfólio] {contact.subject}",
                "text": f"""Nova mensagem do portfólio!

Nome: {contact.name}
Email: {contact.email}

Mensagem:
{contact.message}
""",
            }
        )
    except Exception as error:
        logger.exception("Failed to deliver contact email via Resend")
        raise EmailDeliveryError from error
