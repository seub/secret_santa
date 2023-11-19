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


def send_gmail(subject: str, body: str, recipients: list[str], sender: str = "brice.loustau@gmail.com") -> None:
    logger.info(f"Sending email to {recipients}")

    gmail_settings = get_gmail_settings()
    print(gmail_settings)
    # print(f"{gmail_settings.user_email = }")
    # print(f"{gmail_settings.app_password = }")

    # msg = MIMEMultipart()
    # msg['Subject'] = subject
    # msg['From'] = sender
    # msg['To'] = ", ".join(recipients)
    # msg.attach(MIMEText(body, 'plain'))

    # # Using TLS
    # with smtplib.SMTP('smtp.gmail.com', 587) as server:
    #     server.starttls()  # Secure the connection
    #     server.login(sender, password)
    #     server.send_message(msg)



if __name__ == '__main__':
    send_gmail(
        subject = 'Test Subject', 
        body = 'This is a test email', 
        recipients = ['briceloustau@gmail.com'],
    )