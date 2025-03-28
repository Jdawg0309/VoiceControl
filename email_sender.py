# email_sender.py (Use .env!)
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def send_email():
    try:
        sender_email = os.getenv("EMAIL_USER")
        receiver_email = os.getenv("EMAIL_USER")
        password = os.getenv("EMAIL_PASS")
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "Voice Command Alert"
        msg.attach(MIMEText("Automated message from your Pi.", 'plain'))
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent!")
    except Exception as e:
        print(f"Email error: {e}")