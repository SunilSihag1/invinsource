import smtplib
from email.message import EmailMessage
from config import EMAIL_USER, EMAIL_PASS

def send_mail(receiver_email, subject, content):
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = EMAIL_USER
        msg["To"] = receiver_email
        msg.set_content(content)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
    except Exception as e:
        print("Email error:", e)
