import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from dotenv import load_dotenv

def send_email_with_attachment(file_content, file_name):
    load_dotenv()
    smtp_server = 'smtp-mail.outlook.com'
    smtp_port = 587
    smtp_username = os.getenv('USER_NAME')
    smtp_password = os.getenv('PASSWORD')
    
    from_email = os.environ.get('FROM_EMAIL')
    to_email = os.environ.get('TO_EMAIL')
    subject = 'Latest Medical Consultants/Registrars Report'
    body = 'Please find attached the report.'
            
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body))
        
    attachment = MIMEApplication(file_content, _subtype='csv')
    attachment.add_header('Content-Disposition', 'attachment', filename=file_name)
    msg.attach(attachment)
        
    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(smtp_username, smtp_password)
        smtp.send_message(msg)
