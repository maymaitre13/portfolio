import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

AGIFY_LINK = "https://api.agify.io"
GEN_LINK = "https://api.genderize.io"


def get_age(name):
    data_age = {
        "name": name
    }

    value = requests.get(AGIFY_LINK, params=data_age)
    return str(value.json()["age"])  # Reterning the possible Age


def get_sex(name):
    data_sex = {
        "name" : name
    }

    value = requests.get(GEN_LINK, params=data_sex)
    return str(value.json()["gender"])  # Reterning the Gender


def send_email(fName, lName, email, message):

    # SMTP server settings
    smtp_server = "smtp.mail.yahoo.com"
    smtp_port = 587
    smtp_username = "maelmaitre@yahoo.fr"
    smtp_password = "uztqoahqgklqlwtc"

    # Email message settings
    from_address = smtp_username
    to_address = "merji013@gmail.com"
    subject = "Message from a client"
    body = f"The name of the client {fName} {lName} \n The email of the client :" \
           f"{email} \n Message :"+message

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_address, to_address, msg.as_string())
        print("Email sent successfully!")
