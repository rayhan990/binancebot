# Import smtplib for the actual sending function
import smtplib
from settings import settings

# Import the email modules we'll need
from email.message import EmailMessage

def sendErrorEmail(message, subject):
    try:
        msg = EmailMessage()
        msg.set_content(message)

        msg['Subject'] = subject
        msg['From'] = settings.error_log_email_sender
        msg['To'] = settings.error_log_email_receiver

        s = smtplib.SMTP(settings.smtp_server)
        s.login(settings.smtp_user, settings.smtp_pass)
        s.send_message(msg)
        s.quit
    except Exception as ex:
        print(ex)