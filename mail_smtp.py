from flask_mail import Mail
from flask import Flask 


# Create a Flask app instance
app = Flask(__name__)
mail = Mail(app)




# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'mail.smtp2go.com'
app.config['MAIL_PORT'] = 587  # Use the appropriate port
app.config['MAIL_USE_TLS'] = True  # Enable TLS if required
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'info@mleasd.com'
app.config['MAIL_PASSWORD'] = 'b4lCoLJnCyUJTL2Z'


# Create a Mail instance
mail.init_app(app)


