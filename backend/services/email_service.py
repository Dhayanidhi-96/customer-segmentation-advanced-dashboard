from __future__ import annotations

import smtplib
from email.mime.text import MIMEText

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from config import settings


class EmailService:
    def send_email(self, to_email: str, subject: str, html_content: str) -> None:
        if settings.SENDGRID_API_KEY:
            self._send_sendgrid(to_email, subject, html_content)
            return
        self._send_smtp(to_email, subject, html_content)

    def _send_sendgrid(self, to_email: str, subject: str, html_content: str) -> None:
        message = Mail(
            from_email=(settings.FROM_EMAIL, settings.FROM_NAME),
            to_emails=to_email,
            subject=subject,
            html_content=html_content,
        )
        client = SendGridAPIClient(settings.SENDGRID_API_KEY)
        client.send(message)

    def _send_smtp(self, to_email: str, subject: str, html_content: str) -> None:
        msg = MIMEText(html_content, "html")
        msg["Subject"] = subject
        msg["From"] = settings.FROM_EMAIL
        msg["To"] = to_email

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            if settings.SMTP_USERNAME and settings.SMTP_PASSWORD:
                server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.sendmail(settings.FROM_EMAIL, [to_email], msg.as_string())
