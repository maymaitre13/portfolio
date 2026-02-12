import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- External API endpoints ---
AGIFY_LINK = "https://api.agify.io"
GEN_LINK = "https://api.genderize.io"


# --- Name-based enrichment helpers ---
def get_age(name):
    """Return the estimated age for a given first name."""
    data_age = {"name": name}

    value = requests.get(AGIFY_LINK, params=data_age)
    return str(value.json()["age"])  # Reterning the possible Age


def get_sex(name):
    """Return the estimated gender for a given first name."""
    data_sex = {"name": name}

    value = requests.get(GEN_LINK, params=data_sex)
    return str(value.json()["gender"])  # Reterning the Gender


# --- Contact email delivery via SMTP ---
def send_email(fName, lName, email, message):
    """Send a contact-form email using SMTP settings from environment variables."""
    # SMTP server settings from environment
    smtp_server = os.getenv("SMTP_SERVER", "smtp.mail.yahoo.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = (os.getenv("SMTP_USERNAME") or "").strip()
    smtp_password = (os.getenv("SMTP_PASSWORD") or "").strip()
    smtp_use_ssl = os.getenv("SMTP_USE_SSL", "0") == "1"
    smtp_timeout = int(os.getenv("SMTP_TIMEOUT", "20"))

    # Recipient and optional overrides
    to_address = (os.getenv("CONTACT_TO_ADDRESS") or "").strip()
    from_override = (os.getenv("CONTACT_FROM_ADDRESS") or "").strip()
    from_address = from_override or smtp_username
    subject = (
        os.getenv("CONTACT_SUBJECT", "Message from portfolio contact form") or ""
    ).strip() or "Message from portfolio contact form"

    # Validate required configuration
    missing = [
        name for name, val in [
            ("SMTP_USERNAME", smtp_username),
            ("SMTP_PASSWORD", smtp_password),
            ("CONTACT_TO_ADDRESS", to_address),
        ] if not val
    ]
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    # Build email body
    body = (
        f"The name of the client: {fName} {lName}\n"
        f"The email of the client: {email}\n"
        f"Message: {message}"
    )

    # Create the email message
    msg = MIMEMultipart()
    msg["From"] = from_address
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Establish the SMTP connection and deliver the message.
    # Yahoo supports STARTTLS (587) and SSL/TLS (465).
    use_ssl = smtp_use_ssl or smtp_port == 465
    if use_ssl:
        with smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=smtp_timeout) as server:
            server.login(smtp_username, smtp_password)
            server.sendmail(from_address, to_address, msg.as_string())
        return

    with smtplib.SMTP(smtp_server, smtp_port, timeout=smtp_timeout) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_address, to_address, msg.as_string())
