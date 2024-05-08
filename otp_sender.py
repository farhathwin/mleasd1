import smtplib
from email.mime.text import MIMEText
from config import SMTP_SERVER, SMTP_PORT , SENDER_PASSWORD , SENDER_EMAIL

smtp_server = SMTP_SERVER
smtp_port = SMTP_PORT
sender_email = SENDER_EMAIL
sender_password = SENDER_PASSWORD

def send_otp_email(email, otp, smtp_server, smtp_port, sender_email, sender_password):
    msg = MIMEText(f'Your OTP is: {otp}')
    msg['Subject'] = 'OTP Verification'
    msg['From'] = sender_email
    msg['To'] = email

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, [email], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

