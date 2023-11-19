#!/usr/bin/env python


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import cache
import logging
import smtplib

from pydantic_settings import BaseSettings, SettingsConfigDict



logger = logging.getLogger(__name__)



class GmailSettings(BaseSettings):
    user_email: str
    app_password: str

    model_config = SettingsConfigDict(env_file='gmail_settings.env', env_file_encoding='utf-8')


@cache
def get_gmail_settings() -> GmailSettings:
    return GmailSettings() # type: ignore


def send_gmail(subject: str, body: str, recipients: list[str]) -> None:
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