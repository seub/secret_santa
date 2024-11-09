#!/usr/bin/env python

"""
This module provides functions to send emails using Gmail.

Example usage:
```
export USER_EMAIL="brice.loustau@gmail.com"
export APP_PASSWORD="your_app_password"
python3 -m secret_santa.mail
```

Note: To create an app password: Go to Google Account > Security > 2-Step Verification > App passwords.
"""


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import cache
import logging
import smtplib

from pydantic_settings import BaseSettings



logger = logging.getLogger(__name__)



class GmailSettings(BaseSettings):
    """
    Pydantic model for Gmail settings.
    """

    user_email: str
    app_password: str


@cache
def get_gmail_settings() -> GmailSettings:
    """
    Create and return a GmailSettings instance.
    """
    return GmailSettings() # type: ignore


def send_gmail(subject: str, body: str, recipients: list[str]) -> None:
    """
    Send an email using Gmail.
    """
    logger.info(f"Sending email to {recipients}")

    gmail_settings = get_gmail_settings()
    sender = gmail_settings.user_email
    password = gmail_settings.app_password

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()  # Secure the connection
        server.login(sender, password)
        server.send_message(msg)



if __name__ == '__main__':
    send_gmail(
        subject = 'Test Subject',
        body = 'This is a test email',
        recipients = ['briceloustau@gmail.com'],
    )
