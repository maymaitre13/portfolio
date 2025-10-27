import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

AGIFY_LINK = "https://api.agify.io"
GEN_LINK = "https://api.genderize.io"


def get_age(name):
    data_age = {"name": name}

    value = requests.get(AGIFY_LINK, params=data_age)
    return str(value.json()["age"])  # Reterning the possible Age


def get_sex(name):
    data_sex = {"name": name}

    value = requests.get(GEN_LINK, params=data_sex)
    return str(value.json()["gender"])  # Reterning the Gender


def send_email(fName, lName, email, message):
    # SMTP server settings from environment
    smtp_server = os.getenv("SMTP_SERVER", "smtp.mail.yahoo.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")

    # Recipient and optional overrides
    to_address = os.getenv("CONTACT_TO_ADDRESS")
    from_address = os.getenv("CONTACT_FROM_ADDRESS", smtp_username)
    subject = os.getenv("CONTACT_SUBJECT", "Message from portfolio contact form")

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

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_address, to_address, msg.as_string())
