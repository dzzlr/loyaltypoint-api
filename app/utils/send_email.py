import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger('uvicorn.error')

def send_email(subject: str, recipient_email: str, body: str):
    try:
        msg = MIMEMultipart()
        msg['From'] = os.getenv("EMAIL_FROM")
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))

        # Menghubungkan ke server Mailtrap
        server = smtplib.SMTP(os.getenv("SMTP_HOST"), os.getenv("SMTP_PORT"))
        server.starttls()
        server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASSWORD"))
        
        # Mengirim email
        server.sendmail(os.getenv("EMAIL_FROM"), recipient_email, msg.as_string())
        server.quit()
        logger.info({'message': "Successfully sent voucher code to " + recipient_email})
        # print("Email sent successfully")
    except Exception as e:
        logger.error({
            'message': "Failed sent voucher code to " + recipient_email,
            'error': e})
        # print(f"Failed to send email: {e}")
