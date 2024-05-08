from flask_mail import Message
from mail_smtp import mail , app



def send_registration_email(email, confirmation_link, smtp_server, smtp_port, sender_email, sender_password):
    # Create a Flask-Mail message
    msg = Message('Registration Confirmation', sender=sender_email, recipients=[email])
    
    # Set the email body with the confirmation link
    msg.body = f'Click the following link to confirm your registration: {confirmation_link}'
    
    try:
        # Send the email
        with app.app_context():  # Replace "your_app" with your Flask app instance
            mail.send(msg)
        return True
    except Exception as e:
        # Handle any exceptions that occur during email sending
        print(str(e))
        return False
