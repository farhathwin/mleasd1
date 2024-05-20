
from flask import Flask, render_template, request, redirect , url_for , flash , session , current_app , jsonify
from init_db import User, datetime , Agent , db ,Customer ,CustomerComment ,Lead    
from config import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD
from otp_sender import send_otp_email   
import random , openpyxl 
import os , logging
from user_data_module import fetch_user_data ,fetch_agent_data ,fetch_agent_by_id , fetch_user_by_id
from datetime import timedelta , datetime
from sqlalchemy import create_engine , func , and_
import logging , uuid
from sqlalchemy import text
from send_registration_email import send_registration_email 
from sqlalchemy.exc import IntegrityError , SQLAlchemyError
from PIL import Image
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
from functools import wraps
from sqlalchemy.orm import joinedload


UPLOAD_FOLDER = 'D:/Mleasd New- Project Farhath 07-10-23/static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__, static_url_path='/static')

app.config['DEBUG'] = True
app.config['MAIL_DEBUG'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

#Set the secret key for session management
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')

app.permanent_session_lifetime = timedelta(minutes=45)


otp_storage = {}
registration_tokens = {}



# Set the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mleasd.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://mleasd:7wzhQ4_vAKjQS2#@mleasd.mysql.pythonanywhere-services.com/mleasd$default'
#app.config['SQLALCHEMY_ECHO'] = True


engine = create_engine('sqlite:///mleasd.db')
#session = Session(engine)

#engine = create_engine('mysql+mysqldb://scott:tiger@localhost/foo',pool_recycle=3600)

#engine = create_engine('mysql+mysqldb://scott:tiger@localhost/foo',pool_recycle=3600)

#engine = create_engine('mysql://mleasd:7wzhQ4_vAKjQS2#@mleasd.mysql.pythonanywhere-services.com/mleasd$newmleasd', pool_recycle=3600)
# Initialize the database within the application context


db.init_app(app)
migrate = Migrate(app, db)
with app.app_context():
    db.create_all()
    

# Set the SMTP and email configuratio
smtp_server = SMTP_SERVER
smtp_port = SMTP_PORT
sender_email = SENDER_EMAIL
sender_password = SENDER_PASSWORD


def get_user_id_somehow():
    user_id = session.get('user_id')
    return user_id

@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')


@app.route('/base', methods=['GET'])
def base():
    return render_template('base.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def requires_permission(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Assume the user's ID is stored in the session
            user_id = session.get('user_id')
            user = User.query.get(user_id)
            if not user or not user.has_permission(permission):
                flash('You do not have permission to access this resource.', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator



@app.route('/userprofile', methods=['GET', 'POST'])
def userprofile():
    if 'email' in session:
        email = session['email']
        user = User.query.filter_by(email=email).first()

        if user:
            if request.method == 'POST':
                print("Received POST request")
                print("Form data:", request.form)

                # Update optional details if the form is submitted
                user.trading_name = request.form.get("trading_name")
                user.iata_code = request.form.get("iata_code")
                user.trade_licence = request.form.get("trade_licence")
                user.street_1 = request.form.get("street_1")
                user.street_2 = request.form.get("street_2")
                user.town_city = request.form.get("town_city")
                user.post_code = request.form.get("post_code")
                user.state_province = request.form.get("state_province")
                user.country = request.form.get("country")

                # Fetch the business_phone_with_code from the form
                # Fetch the business_phone_with_code from the form
                business_phone_with_code = request.form.get("business_phone")

                # Check if business_phone_with_code is not None
                if business_phone_with_code is not None:
                    # Split the business_phone_with_code using the first space as a delimiter
                    parts = business_phone_with_code.split(" ", 1)

                    # Check if the split produced two parts
                    if len(parts) == 2:
                        country_code, phone_number = parts

                        # Remove any non-numeric characters from the phone number
                        phone_number = ''.join(filter(str.isdigit, phone_number))

                        # Set the user's business_phone with the formatted phone number
                        user.business_phone = f"{country_code} {phone_number}"
                    else:
                        # Handle the case where the input format is not as expected
                        print("Invalid format for business_phone_with_code")
                else:
                    # Handle the case where business_phone_with_code is None
                    print("business_phone_with_code is None")

                # Do not apply capitalization to email and website
                user.business_email = request.form.get("business_email")
                user.website = request.form.get("website")

                db.session.commit()

                print("Profile updated successfully")
                flash("Profile updated successfully", "success")

                # Handle logo upload
                if "logo" in request.files:
                    logo_file = request.files["logo"]
                    if logo_file.filename and allowed_file(logo_file.filename):
                        try:
                            # Save the logo file to the upload folder
                            logo_filename = secure_filename(logo_file.filename)
                            logo_path = os.path.join(app.config["UPLOAD_FOLDER"], logo_filename)
                            logo_file.save(logo_path)

                            # Resize the image to 200x200 pixels
                            logo_image = Image.open(logo_path)
                            logo_image.thumbnail((200, 200))
                            logo_image.save(logo_path)

                            # Update the user model with additional logo information
                            user.logo_data = logo_file.read()  # Store the binary data of the image
                            user.logo_filename = logo_filename
                            user.logo_mime_type = logo_file.mimetype

                            db.session.commit()

                            print("Logo updated successfully")
                            flash("Logo updated successfully", "success")
                        except Exception as e:
                            print(f"Error processing image: {e}")
                            flash("Error processing image", "danger")
                    else:
                        flash("Invalid file format. Allowed formats are: png, jpg, jpeg, gif", "danger")

                return redirect(url_for("userprofile"))

            # Fetch the list of Users associated with the user's ID
            user_profile = User.query.filter_by(id=user.id).all()
            return render_template('profile_user.html', user=user, user_profile=user_profile)

        else:
            flash('User not found.', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Please log in to access the user list.', 'danger')
        return redirect(url_for('login'))


@app.route('/agentprofile', methods=['GET', 'POST'])
def agentprofile():
    if 'email' in session:
        email = session['email']
        agent = fetch_agent_data(email)

        if agent:
            if request.method == 'POST':
                print("Received POST request")
                print("Form data:", request.form)

                # Fetch the existing agent profile by querying with the agent's ID
                agent_id = agent.id
                agent = Agent.query.get(agent_id)

                if agent:
                    # Update optional details if the form is submitted
                    agent.trading_name = request.form.get("trading_name")
                    agent.street_1 = request.form.get("street_1")
                    agent.street_2 = request.form.get("street_2")
                    agent.town_city = request.form.get("town_city")
                    agent.post_code = request.form.get("post_code")
                    agent.state_province = request.form.get("state_province")
                    agent.country = request.form.get("country")
                    

                    # Fetch the business_phone_with_code from the form
                    business_phone_with_code = request.form.get("business_phone")

                    # Check if business_phone_with_code is not None
                    if business_phone_with_code is not None:
                        # Split the business_phone_with_code using the first space as a delimiter
                        parts = business_phone_with_code.split(" ", 1)

                        # Check if the split produced two parts
                        if len(parts) == 2:
                            country_code, phone_number = parts

                            # Remove any non-numeric characters from the phone number
                            phone_number = ''.join(filter(str.isdigit, phone_number))
                            # Set the agent's business_phone with the country code
                            agent.business_phone = f"{country_code} {phone_number}"
                        else:
                            # Handle the case where the input format is not as expected
                            print("Invalid format for business_phone_with_code")
                    else:
                        # Handle the case where business_phone_with_code is None
                        print("business_phone_with_code is None")

                    # Do not apply capitalization to email and website
                    agent.business_email = request.form.get("business_email")
                    agent.website = request.form.get("website")

                    db.session.commit()
                    print("Profile updated successfully")
                    flash("Profile updated successfully", "success")

                    # Handle logo upload
                    if "logo" in request.files:
                        logo_file = request.files["logo"]
                        if logo_file.filename and allowed_file(logo_file.filename):
                            try:
                                # Save the logo file to the upload folder
                                logo_filename = secure_filename(logo_file.filename)
                                logo_path = os.path.join(app.config["UPLOAD_FOLDER"], logo_filename)
                                logo_file.save(logo_path)

                                # Resize the image to 200x200 pixels
                                logo_image = Image.open(logo_path)
                                logo_image.thumbnail((200, 200))
                                logo_image.save(logo_path)

                                # Update the agent model with additional logo information
                                agent.logo_data = logo_file.read()  # Store the binary data of the image
                                agent.logo_filename = logo_filename
                                agent.logo_mime_type = logo_file.mimetype

                                db.session.commit()

                                print("Logo updated successfully")
                                flash("Logo updated successfully", "success")
                            except Exception as e:
                                print(f"Error processing image: {e}")
                                flash("Error processing image", "danger")
                        else:
                            flash("Invalid file format. Allowed formats are: png, jpg, jpeg, gif", "danger")
                else:
                    print("Agent not found.")
                    flash("Agent not found.", "danger")

                return redirect(url_for("agentprofile"))

            # Fetch the list of Users associated with the user's ID
            agent_profile = Agent.query.filter_by(id=agent.id).all()
            return render_template('profile_agent.html', user=agent, agent_profile=agent_profile)

        else:
            flash('User not found.', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Please log in to access the user list.', 'danger')
        return redirect(url_for('login'))
    



@app.before_request
def before_request():
    # Refresh the session if the user is logged in
    if 'logged_in' in session:
        session.modified = True



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        business_name = request.form['business_name']

        # Check if email already exists in the system
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please log in.', 'warning')
            return redirect(url_for('login'))  # or return to the registration page

        # New company or existing company check
        
        existing_company = User.query.filter(User.email).first()
            

        if existing_company:
            flash('This domain is already registered with another company.', 'warning')
            return redirect(url_for('register'))

        last_company_id = db.session.query(func.max(User.company_id)).scalar()
        if last_company_id:
            next_company_number = int(last_company_id[2:]) + 1
            company_id = f'ML{next_company_number:04d}'
        else:
            company_id = 'ML0001'

        # Generate user_id
        last_user_id_within_company = db.session.query(func.max(User.user_id)).filter_by(company_id=company_id).scalar()
        user_id = (last_user_id_within_company + 1) if last_user_id_within_company else 1
        
        # Generating a random OTP
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])

        try:
            new_user = User(
                user_id=user_id,
                company_id=company_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                business_name=business_name,
                otp=otp,
                is_verified=False
            )
            db.session.add(new_user)
            db.session.commit()

            if send_otp_email(email, otp, smtp_server, smtp_port, sender_email, sender_password):
                session['email'] = email
                session['user_id'] = new_user.id
                flash('An OTP has been sent to your email. Please check your inbox and verify your account.', 'success')
                return redirect(url_for('verify', model_type='user'))
            else:
                flash('Error sending OTP. Please try again later.', 'danger')
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Registration error: {e}")
            flash('An error occurred during registration. Please try again later.', 'danger')

        return redirect(url_for('register'))

    return render_template('register.html')




@app.route('/register-agent', methods=['GET', 'POST'])
def register_agent():
    #new_agent = None
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        business_name = request.form.get('business_name')
        agent_business_name = request.form.get('agent_business_name')

        print(f"Email received in register_agent: {email}")

        try:


        # Check if the email is already registered
            existing_user = User.query.filter_by(email=email).first()
            existing_master_subuser = User.query.filter_by(email=email).first()
            existing_agent = Agent.query.filter_by(email=email).first()

            if existing_user or existing_master_subuser or existing_agent:
            # Check if the email is registered under the same company (business name)
                if (
                    (existing_user and existing_user.business_name == business_name) or
                    (existing_master_subuser and existing_master_subuser.user.business_name == business_name) or
                    (existing_agent and existing_agent.user.business_name == business_name)
                ):
                    flash('Email address is already registered under this company.', 'danger')
                else:
                    flash('Email address is already registered under a different company. Please use a different email.', 'danger')
            else:
                # Generate a random 6-digit OTP
                logging.debug("Generating OTP...")
                otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
                logging.debug(f"Generated OTP: {otp}")

                user = User.query.filter_by(business_name=business_name).first()
                if user is None:

                    flash('No matching user found for the specified business name.', 'danger')
                    return render_template('register_agent.html')
                
                session['email'] = email         
                
                    
            
                agent = Agent(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    otp=otp,
                    business_name=business_name,  # Use the 'business_name' from the form data
                    agent_business_name= agent_business_name 
                )
                
                # Generate PCC code and associate with the user
                agent.generate_pcc_code()
                

                # Add the Agent instance to the session
                db.session.add(agent)
                agent.user = user
                db.session.commit()
               
                new_agent = Agent.query.filter_by(email=email).first()

                if new_agent:

                    if send_otp_email(email, otp, smtp_server, smtp_port, sender_email, sender_password):
                        session['user_id'] = new_agent.id  # Store user ID in the session
                        session['model_type'] = 'agent'

                        flash('An OTP has been sent to your email. Please check your inbox and verify your account.', 'success')
                        return redirect(url_for('verify', model_type='agent'))
                    else:
                        flash('Error sending OTP. Please try again later.', 'danger')
                else:
                    flash('Agent object not found.', 'danger')
        
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            flash('Error: {}'.format(str(e)), 'danger')
            return render_template('register_agent.html')
       
    # Render the registration form with the list of business names
    unique_business_names = db.session.query(User.business_name).distinct().all()
    business_names = [name[0] for name in unique_business_names]
    return render_template('register_agent.html', business_names=business_names)


@app.route('/register-subuser', methods=['GET', 'POST'])
def register_subuser():
    if 'user_id' not in session or 'company_id' not in session:
        flash('Please log in again.', 'warning')
        return redirect(url_for('login'))

    company_id = session['company_id']
    business_name = session['business_name']
    existing_subusers_count = User.query.filter_by(company_id=company_id).count()
    new_user_id = existing_subusers_count + 1

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])

        try:
            existing_user = User.query.filter_by(email=email).first()

            if existing_user:
                flash('Email address is already registered. Please use a different email.', 'email-danger')
            else:
                new_subuser = User(
                    user_id=new_user_id,
                    company_id=session['company_id'],
                    first_name=first_name,
                    last_name=last_name,
                    business_name= business_name,
                    email=email,
                    otp=otp,
                    is_verified=False
                )

                db.session.add(new_subuser)
                db.session.commit()

                registration_token = str(uuid.uuid4())
                otp_storage[email] = {'otp': otp, 'expiration': datetime.now() + timedelta(minutes=15)}
                registration_tokens[registration_token] = email

                confirmation_link = url_for('confirm_registration', token=registration_token, _external=True)

                print(confirmation_link)

                if send_registration_email(email, confirmation_link, smtp_server, smtp_port, sender_email, sender_password):
                    flash('A registration link has been sent to your email. Please check your inbox and verify your account.', 'success')
                    session['email'] = session.get('email', email)
                    return redirect(url_for('userlist'))
                else:
                    flash('Error sending the registration email. Please try again later.', 'danger')

        except IntegrityError:
            flash('Email address is already registered. Please use a different email.', 'email-danger')

    user = None
    if 'email' in session:
        email = session['email']
        user = fetch_user_data(email)

    return render_template('register_user.html', user=user)

@app.route('/register-agent-subuser', methods=['GET', 'POST'])
def register_agent_subuser():
    print("Inside register_agent_subuser function")
    if 'user_id' not in session:
        flash('Please log in before registering a master subuser.', 'warning')
        return redirect(url_for('login'))  # Redirect to your login page

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        user_id = session['user_id']

        # Generate a random 6-digit OTP
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])

        # Check if the email already exists in the database
        existing_user = Agent.query.filter_by(email=email).first()

        if existing_user:
            flash('Email address is already registered. Please use a different email.', 'danger')
        else:
            # Create the master_subuser record with the user_id and generated OTP
            agent_subuser = Agent(
                first_name=first_name,
                last_name=last_name,
                otp=otp,
                is_verified=0,
                email=email,
                agent_id=user_id
            )

            # Add and commit the record to the database
            db.session.add(agent_subuser)
            db.session.commit()


            def get_model_type(email):
                if User.query.filter_by(email=email).first():
                    return 'user'
                
                elif Agent.query.filter_by(email=email).first():
                    return 'agent'
                
                else:
                    return None
            registration_token = str(uuid.uuid4())

            # Save the OTP and registration token in temporary storage
            otp_storage[email] = {'otp': otp, 'expiration': datetime.now() + timedelta(minutes=15)}
            registration_tokens[registration_token] = email

            # Construct the registration confirmation link
            confirmation_link = url_for('confirm_registration', token=registration_token, _external=True)

            # Send the registration email with the confirmation link
            if send_registration_email(email, confirmation_link, smtp_server, smtp_port, sender_email, sender_password):
                flash('A registration link has been sent to your email. Please check your inbox and verify your account.', 'success')

                # Keep or set the session email after registration
                session['email'] = session.get('email', email)

                print("Redirecting to subagent_userlist")
                return redirect(url_for('subagent_userlist'))  # Redirect to the user list page after successful registration
            else:
                flash('Error sending the registration email. Please try again later.', 'danger')
    user = None
    if 'email' in session:
        email = session['email']
        user = fetch_agent_data(email)
        
    print("Rendering register_agent_subuser.html")
    print("Session content before redirect:", session)
    return render_template('register_agent_subuser.html', user=user)
    

# Registration confirmation route
@app.route('/confirm-registration/<token>', methods=['GET'])
def confirm_registration(token):
    email = registration_tokens.get(token)

    if not email:
        flash('Invalid registration link. Please request a new link.', 'danger')
        return redirect(url_for('login'))  # Redirect to the login page

    otp_data = otp_storage.get(email)
    if not otp_data or datetime.now() > otp_data['expiration']:
        flash('The registration link has expired. Please request a new link.', 'danger')
        return redirect(url_for('login'))  # Redirect to the login page

    # Generate a new OTP for the user
    new_otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])

    # Store the new OTP in the OTP storage
    otp_storage[email] = {'otp': new_otp, 'expiration': datetime.now() + timedelta(minutes=15)}

    # Send the OTP email
    if send_otp_email(email, new_otp , smtp_server, smtp_port, sender_email, sender_password):
        flash('A new OTP has been sent to your email. Please check your inbox and verify your account.', 'success')
        return render_template('confirm_registration.html', email=email, token=token)
    else:
        flash('Error sending OTP. Please try again later.', 'danger')
        return redirect(url_for('login'))
    

@app.route('/complete-registration/<token>', methods=['POST'])
def complete_registration(token):
    email = registration_tokens.get(token)
    otp_data = otp_storage.get(email)

    if not email or not otp_data or datetime.now() > otp_data['expiration']:
        flash('Invalid registration link. Please request a new link.', 'danger')
        return redirect(url_for('login'))  # Redirect to the login page

    user_otp = request.form.get('otp')  # Get OTP entered by the user

    if user_otp == otp_data['otp']:
        # Valid OTP, complete the user registration process
        # ... (code to create the user, update the database, etc.)

        # Remove the OTP and registration token from storage
        del otp_storage[email]
        del registration_tokens[token]

        flash('Registration complete. You can now log in.', 'success')
        return redirect(url_for('login'))  # Redirect to the login page
    else:
        flash('Invalid OTP. Please try again.', 'danger')
        return render_template('confirm_registration.html', email=email, token=token)

#Handle OTP validation and user creation on the confirmation page
@app.route('/confirm-registration/<token>', methods=['POST'])
def handle_confirmation(token):
    email = registration_tokens.get(token)

    if not email:
        flash('Invalid registration link. Please request a new link.', 'danger')
        return redirect(url_for('login'))  # Redirect to the login page

    otp_data = otp_storage.get(email)
    if not otp_data or datetime.now() > otp_data['expiration']:
        flash('The registration link has expired. Please request a new link.', 'danger')
        return redirect(url_for('login'))  # Redirect to the login page

    user_otp = request.form.get('otp')  # Get OTP entered by the user

    if user_otp == otp_data['otp']:
        # Valid OTP, complete the user registration process
        # ... (code to create the user, update the database, etc.)

        # Remove the OTP and registration token from storage
        del otp_storage[email]
        del registration_tokens[token]

        flash('Registration complete. You can now log in.', 'success')
        return redirect(url_for('login'))  # Redirect to the login page

    flash('Invalid OTP. Please try again.', 'danger')
    return redirect(url_for('confirm_registration', token=token))


#Mster Subuser list 
@app.route('/userlist', methods=['GET'])
def userlist():
    if 'email' in session:
        email = session['email']
        user = fetch_user_data(email)  # Fetch user data based on email
        if user:
            # Fetch the list of Users associated with the company's ID
            users = User.query.filter_by(company_id=user.company_id).all()
            return render_template('userlist.html', user=user, users=users)
        else:
            flash('User not found.', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Please log in to access the user list.', 'danger')
        return redirect(url_for('login'))
    
@app.route('/manage_userlist/<user_id>', methods=['POST'])
def manage_userlist(user_id):
    with current_app.app_context():
        print(f"Received user_id: {user_id}")  # Check the user_id received

        user = User.query.get(user_id)
        if user:
            action = request.form.get('action')
            if action == 'suspend':
                user.is_verified = False
                flash('Agent suspended successfully!', 'success')
            elif action == 'activate':
                user.is_verified = True
                flash('Agent activated successfully!', 'success')
            else:
                flash('Invalid action specified.', 'danger')

            db.session.commit()
        else:
            flash('User details not found.', 'danger')
            print("User details not found.")  # Log the issue for further investigation

        return redirect(url_for('userlist'))

@app.route('/subagent_userlist', methods=['GET'])
def subagent_userlist():
    if 'email' in session:
        email = session['email']
        agent = fetch_agent_data(email)  # Fetch user data based on email
        if agent:
            # Fetch the list of Users associated with the user's ID
            agent_subusers = Agent.query.filter_by(agent_id=agent.id).all()
            return render_template('subagent_userlist.html', user=agent, agent_subusers=agent_subusers)
        else:
            flash('User not found.', 'danger')
            return redirect(url_for('login'))

    else:
        flash('Please log in to access the user list.', 'danger')
        return redirect(url_for('login'))

# Add the @app.route decorator for the manage_subagent_userlist route
@app.route('/manage_subagent_userlist/<user_id>', methods=['POST'])
def manage_subagent_userlist(user_id):
    with current_app.app_context():
        print(f"Received user_id: {user_id}")

        user = Agent.query.get(user_id)
        if user:
            action = request.form.get('action')
            if action == 'suspend':
                user.is_verified = False
                flash('Agent suspended successfully!', 'success')
            elif action == 'activate':
                user.is_verified = True
                flash('Agent activated successfully!', 'success')
            else:
                flash('Invalid action specified.', 'danger')

            db.session.commit()
        else:
            flash('User details not found.', 'danger')
            print("User details not found.")

        return redirect(url_for('subagent_userlist'))



@app.route('/agentlist', methods=['GET'])
def agentlist():
    if 'email' in session:
        email = session['email']
        user = fetch_user_data(email)  # Fetch user data based on email
        if user:
            # Fetch the list of Agents associated with the user's ID
            agent_list = Agent.query.filter_by(user_id=user.id).all()
            return render_template('agentlist.html', user=user, agent_list=agent_list)
        else:
            flash('User not found.', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Please log in to access the user list.', 'danger')
        return redirect(url_for('login'))

@app.route('/manage_agent/<user_id>', methods=['POST'])
def manage_agent(user_id):
    with current_app.app_context():
        print(f"Received user_id: {user_id}")  # Check the user_id received

        agent = Agent.query.get(user_id)
        if agent:
            action = request.form.get('action')
            if action == 'suspend':
                agent.is_verified = False
                flash('Agent suspended successfully!', 'success')
            elif action == 'activate':
                agent.is_verified = True
                flash('Agent activated successfully!', 'success')
            else:
                flash('Invalid action specified.', 'danger')

            db.session.commit()
        else:
            flash('Agent details not found.', 'danger')
            print("Agent details not found.")  # Log the issue for further investigation

        return redirect(url_for('agentlist'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    model_type = None
    
    if request.method == 'POST':
        email = request.form.get('email')
        model_type = request.form.get('model_type')

        user = User.query.filter_by(email=email).first()
        
        agent = Agent.query.filter_by(email=email).first()
        

        if user:
            model_type = 'user'
        
        elif agent:
            model_type = 'agent'
        
        else:
            flash('Email address not found. Please register first.', 'danger')

        if model_type:
            new_otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            
            if model_type == 'user':
                user.otp = new_otp
                user.date = datetime.utcnow()
                user.time = datetime.now().strftime("%H:%M:%S")
                if user:
                    session['user_id'] = user.id
            
            elif model_type == 'agent':
                agent.otp = new_otp
                agent.date = datetime.utcnow()
                agent.time = datetime.now().strftime("%H:%M:%S")
                if agent:
                    session['user_id'] = agent.id
            
            db.session.commit()

            if send_otp_email(email, new_otp, SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD):
                session['email'] = email
                session['model_type'] = model_type

                url = url_for('verify', model_type=model_type)
                return redirect(url)
            else:
                flash('Error sending OTP. Please try again later.', 'danger')

    return render_template('login.html', model_type=model_type)


@app.route('/verify/<model_type>', methods=['GET', 'POST'])
def verify(model_type):
    email = session.get('email')
    print(f"Email from session: {email}")  # Add this line for debugging

    if request.method == 'POST':
        entered_otp = request.form.get('otp')

        if not email:
            flash('Email not found in session.', 'danger')
            return redirect(url_for('login'))

        # Choose the appropriate model based on 'model_type'
        if model_type == 'user':
            model = User
        elif model_type == 'agent':
            model = Agent
        else:
            flash('Invalid model type.', 'danger')
            return redirect(url_for('login'))

        try:
            user = model.query.filter_by(email=email).first()
            print('Verify user', user)  # Add this line for debugging
            if user:
                if entered_otp == user.otp:
                    user.is_verified = True
                    db.session.commit()

                    session['model_type'] = model_type
                    session['email'] = email

                    # Fetch the company ID based on the user's email and store it in the session
                    company_id = user.company_id
                    session['company_id'] = company_id
                    user_id = user.user_id
                    session['user_id'] = user_id
                    business_name = user.business_name
                    session['business_name'] = business_name
                    
                    print ('Versify Sesson ',company_id)

                    flash(f'{model_type.capitalize()} account verified!', 'success')
                    return redirect(url_for('dashboard'))  # Redirect to the dashboard after verification
                else:
                    flash('Invalid OTP. Please try again.', 'danger')
            else:
                flash('User not found.', 'danger')
        except Exception as e:
            print(f'Error querying the database: {e}')
            flash('Error verifying the account. Please try again later.', 'danger')

    return render_template('verify.html', model_type=model_type)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'email' in session:
        email = session['email']
        user = fetch_user_data(email) # Fetch user data based on email
        if user:
            # Implement logic specific to the master dashboard
            # Fetch additional data if required
            return render_template('dashboard.html', user=user)
        else:
            flash('User not found.', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Please log in to access the dashboard.', 'danger')
        return redirect(url_for('login'))


@app.route('/agent_dashboard', methods=['GET'])
def agent_dashboard():
    # Implement agent dashboard logic here
    if 'email' in session:
        email = session['email']
        user = fetch_agent_data(email)  # Fetch agent data based on email
        if user:
            # Implement logic specific to the agent dashboard
            # Fetch additional data if required
            return render_template('agent_dashboard.html', user=user)
        else:
            flash('Agent data not found.', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Please log in to access the dashboard.', 'danger')
        return redirect(url_for('login'))


@app.route('/customer-create', methods=['GET', 'POST'])
def customer_create():
    if 'user_id' not in session or 'company_id' not in session:
        flash('Please log in again.', 'warning')
        return redirect(url_for('login'))

    company_id = session['company_id']

    user_id = session['user_id']

    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone_no = request.form.get('phone_no')

        phone_no_with_country_code = phone_no   

        # Check if the phone number already exists for the current company
        existing_customer_phone = Customer.query.filter(Customer.company_id == company_id, Customer.phone_no == phone_no_with_country_code).first()
        if existing_customer_phone:
            flash('Customer with the provided phone number already exists within your company.', 'danger')
            return jsonify({'success': False, 'message': 'Duplicate customer phone number within your company.'}), 400

        # Generate new customer ID
        max_customer_id = Customer.query.filter_by(company_id=company_id).with_entities(func.max(Customer.customer_id)).scalar()
        next_customer_id = int(max_customer_id[3:]) + 1 if max_customer_id and max_customer_id.startswith("CUS") else 1
        formatted_customer_id = f"CUS{next_customer_id:04}"

        try:
            new_customer = Customer(
                user_id=user_id,
                company_id=company_id,
                customer_id=formatted_customer_id,
                full_name=full_name,
                email=email,
                phone_no=phone_no_with_country_code,
                is_verified=True,
                is_leads=False  # New customers are not leads by default
            )
            db.session.add(new_customer)
            db.session.commit()
            flash('Customer created successfully.', 'success')
            # After successfully creating a new customer
            return jsonify({'success': True, 'customer_id': formatted_customer_id, 'customer_name': full_name})

        except IntegrityError as e:
            db.session.rollback()
            flash(f'Error creating customer: {str(e)}. Please try again.', 'danger')
            return jsonify({'success': False, 'message': f'Error creating customer: {str(e)}. Please try again.'}), 500

    # Prepare user data for rendering if it's a GET request
    user = None
    if 'email' in session:
        email = session['email']
        user = fetch_user_data(email)

    return render_template('customer_create.html', user=user)

@app.route('/bulk-upload', methods=['GET', 'POST'])
def bulk_upload():
    # Ensure user is logged in
    if 'user_id' not in session or 'company_id' not in session:
        flash('Please log in again.', 'warning')
        return redirect(url_for('login'))
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and file.filename.endswith('.xlsx'):
            filename = secure_filename(file.filename)
            filepath = os.path.join('uploads', filename)
            file.save(filepath)
            try:
                process_excel_file(filepath, session['company_id'], session['user_id'])
                flash('Customers uploaded successfully.', 'success')
            except Exception as e:
                flash(f'Error processing file: {e}', 'danger')
            finally:
                os.remove(filepath)
            return redirect(url_for('customer_leads_list'))
        else:
            flash('Invalid file format, please upload an .xlsx file.')
            return redirect(request.url)
    else:
        # For GET requests, you might want to show the upload form or redirect
    
        return render_template('bulk_upload_form.html')

def generate_customer_id(company_id):
    max_customer_id = Customer.query.filter_by(company_id=company_id).with_entities(func.max(Customer.customer_id)).scalar()
    if max_customer_id:
        if max_customer_id.startswith("CUS"):
            next_customer_id = int(max_customer_id[3:]) + 1
        else:
            next_customer_id = int(max_customer_id) + 1
    else:
        next_customer_id = 1
    return f"CUS{next_customer_id:04}"

def process_excel_file(filepath, company_id, user_id):
    app.logger.info(f'Starting to process Excel file: {filepath}')  # Log the start of the process
    wb = openpyxl.load_workbook(filepath)
    ws = wb.active

    company_id = session['company_id']
    user_id = session['user_id']
    lead_type = None
    marketing_type = None

    for row in ws.iter_rows(min_row=2):  # Assuming first row contains headers
        full_name, email, phone_no = (cell.value for cell in row)
        phone_no = f"+{str(phone_no)}"  # Adjust based on your needs
        customer_id = generate_customer_id(company_id)
        
        
        try:
            new_customer = Customer(
                user_id=user_id,
                company_id=company_id,
                customer_id=customer_id,
                full_name=full_name,
                email=email,
                phone_no=phone_no,
                lead_type=lead_type,
                marketing_type=marketing_type,
                is_verified=True,
                is_leads=True
            )
            db.session.add(new_customer)
            db.session.commit()  # Commit each customer addition to handle errors more gracefully
            app.logger.info(f'Added customer: {new_customer.customer_id}')
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error adding customer {email}: {e}")
            continue  # Skip to the next row, but log the error

    try:
        app.logger.info('All customers processed successfully.')
    except Exception as e:
        app.logger.error(f"Error committing changes to the database: {e}")
    finally:
        wb.close()

@app.route('/customers_list', methods=['GET'])
def customers_list():
    if 'email' in session:
        email = session['email']
        user = fetch_user_data(email)  # Fetch user data based on email
        
        if user:
            # Fetch the list of Customers associated with the user's company ID
            customers = Customer.query.filter_by(company_id=user.company_id).all()
            return render_template('customers_list.html', user=user, customers_list=customers)  # Pass 'customers_list' instead of 'customers'
        else:
            flash('User not found.', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Please log in to access the user list.', 'danger')
        return redirect(url_for('login'))

from sqlalchemy.orm import joinedload

@app.route('/customer-leads-list', methods=['GET', 'POST'])
def customer_leads_list():
    if 'user_id' not in session or 'company_id' not in session:
        flash('Please log in again.', 'warning')
        return redirect(url_for('login'))

    current_company_id = session['company_id']

    # Explicitly join Lead and Customer and filter by company_id for both.
    leads = Lead.query \
        .join(Customer, Lead.customer_id == Customer.customer_id) \
        .filter(Lead.company_id == current_company_id,
                Customer.company_id == current_company_id) \
        .options(joinedload(Lead.customer)) \
        .all()

    users = User.query.filter_by(company_id=current_company_id).all()

    if request.method == 'POST':
        selected_leads = request.form.getlist('selected_leads')
        target_user_id = request.form['target_user_id']
        target_user = User.query.filter_by(id=target_user_id, company_id=current_company_id).first()

        if not target_user:
            flash('Invalid operation. User does not belong to your company.', 'danger')
            return redirect(url_for('customer_leads_list'))

        for lead_id in selected_leads:
            lead = Lead.query.filter_by(id=lead_id, company_id=current_company_id).first()
            if lead:
                lead.user_id = target_user.id
                db.session.add(lead)

        try:
            db.session.commit()
            flash('Leads transferred successfully.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error transferring leads: {e}', 'danger')

        return redirect(url_for('customer_leads_list'))

    return render_template('customer_leads_list.html', leads=leads, users=users)



@app.route('/update-leads/<lead_id>', methods=['GET', 'POST'])
def update_leads(lead_id):
    if 'user_id' not in session or 'company_id' not in session:
        flash('Please log in again.', 'warning')
        return redirect(url_for('login'))

    user_id = session['user_id']
    company_id = session['company_id']

    # Fetch the lead with an explicit join to Customer, specifying the join condition
    lead = Lead.query \
        .join(Customer, and_(Lead.customer_id == Customer.customer_id, Customer.company_id == company_id)) \
        .filter(Lead.lead_id == lead_id, Lead.company_id == company_id) \
        .options(joinedload(Lead.customer)) \
        .first()

    if not lead:
        flash('No lead found or you do not have permission to view this lead.', 'danger')
        return redirect(url_for('dashboard'))

    if lead.customer:
        print(f"Customer Loaded: ID {lead.customer.customer_id}, Company ID {lead.customer.company_id}")

    if request.method == 'POST':
        comment_text = request.form.get('comment')
        if not comment_text:
            flash('Comment cannot be empty.', 'warning')
            return redirect(url_for('update_leads', lead_id=lead_id))

        new_comment = CustomerComment(
            lead_id=lead.lead_id,
            company_id=company_id,
            created_by=user_id,
            comment=comment_text,
            created_at=datetime.utcnow()
        )
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added to lead successfully.', 'success')
        return redirect(url_for('update_leads', lead_id=lead_id))

    
    #print(f"Attempting to fetch comments for lead_id: {lead_id} and company_id: {company_id}")

    # Test fetching all comments for Lead ID to see if any exist at all
    

    comments = CustomerComment.query \
        .join(User, and_(CustomerComment.created_by == User.user_id, User.company_id == company_id)) \
        .filter(
            CustomerComment.lead_id == lead.lead_id,
            CustomerComment.company_id == company_id  # This ensures comments are linked to the correct company
        ) \
        .order_by(CustomerComment.created_at.desc()) \
        .all()

    # Define the query without executing it
    query = CustomerComment.query \
        .join(User, and_(CustomerComment.created_by == User.user_id, User.company_id == company_id)) \
        .filter(
            CustomerComment.lead_id == lead.lead_id,
            CustomerComment.company_id == company_id
        ) \
        .order_by(CustomerComment.created_at.desc())

    # Print the raw SQL query
    print(str(query.statement.compile(compile_kwargs={"literal_binds": True})))

    # Now execute the query to get the results
    comments = query.all()

    # You can now iterate over comments or pass them to your template
    print(f"Comments found: {len(comments)}")
    for comment in comments:
        print(f"Comment ID: {comment.id}, Posted by User ID: {comment.created_by}, User's Company ID: {comment.user.company_id}")

    print(f"Filtered Comments: {len(comments)}")
    for comment in comments:
        print(f"Comment by {comment.user.first_name}: {comment.comment}")   


    print(f"Comments found: {len(comments)}")
    for comment in comments:
        print(f"Comment ID: {comment.id}, Posted by User ID: {comment.created_by}, User's Company ID: {comment.company_id}")

    return render_template('update_lead.html', lead=lead, customer=lead.customer, comments=comments)








@app.route('/create-leads', methods=['GET', 'POST'])
def create_leads():
    if 'user_id' not in session or 'company_id' not in session:
        flash('Please log in again.', 'warning')
        return redirect(url_for('login'))

    company_id = session['company_id']
    user_id = session['user_id']

    # Fetch customers from the database
    customers = Customer.query.filter_by(company_id=company_id).all()  # Ensure you have the Customer model defined correctly

    if request.method == 'POST':
        new_lead_id = Lead.generate_lead_id(company_id)
        customer_id = request.form.get('customer_id')
        lead_type = request.form.get('lead_type')
        marketing_type = request.form.get('marketing_type')

        if customer_id:
            # Create a new lead
            new_lead = Lead(company_id=company_id, user_id=user_id, customer_id=customer_id, 
                            lead_type=lead_type, marketing_type=marketing_type , lead_id=new_lead_id)
            db.session.add(new_lead)
            db.session.commit()
            flash('Lead created successfully.', 'success')
            # Redirect to a view that shows all leads
            return redirect(url_for('customer_leads_list'))  # Assume 'view_leads' is the endpoint that shows all leads
        flash('No customer selected or found.', 'danger')
        return redirect(url_for('create_leads'))

    # Pass customers to the template
    return render_template('create_leads.html', customers=customers)





@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/check-db-connection', methods=['GET'])
def check_db_connection():
    try:
        # Attempt to establish a database connection and execute a simple query
        db.session.execute(text('SELECT 1'))
        return 'Database connection is OK'
    except Exception as e:
        return f'Database connection error: {str(e)}', 500  
    

    


if __name__ == "__main__":
    app.run(debug=True)
