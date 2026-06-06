import smtplib
from email.message import EmailMessage
from pathlib import Path

from app.config import settings


def send_email_with_attachment(recipient_email: str, subject: str, body: str, attachment_path: Path) -> None:
    message = EmailMessage()
    message["From"] = settings.smtp_user
    message["To"] = recipient_email
    message["Subject"] = subject
    message.set_content(body)
    message.add_attachment(
        attachment_path.read_bytes(),
        maintype="application",
        subtype="pdf",
        filename=attachment_path.name,
    )
    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        server.starttls()
        server.login(settings.smtp_user, settings.smtp_password)
        server.send_message(message)
