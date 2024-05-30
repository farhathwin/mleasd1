

from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import validates , relationship
from sqlalchemy import LargeBinary 
from flask_sqlalchemy import SQLAlchemy
import re


db = SQLAlchemy()
def init_db(app):
    db.init_app(app)

# Models 

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    company_id = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    otp = db.Column(db.String(6), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    time = db.Column(db.String(10), default=datetime.now().strftime("%H:%M:%S"))
    business_name = db.Column(db.String(50), nullable=False)
    trading_name = db.Column(db.String(50))
    iata_code = db.Column(db.String(50))
    trade_licence = db.Column(db.String(50))
    street_1 = db.Column(db.String(100))
    street_2 = db.Column(db.String(100))
    town_city = db.Column(db.String(50))
    state_province = db.Column(db.String(50))
    post_code = db.Column(db.String(50))
    country = db.Column(db.String(50))
    business_phone = db.Column(db.String(20))
    business_email = db.Column(db.String(120))
    website = db.Column(db.String(100))
    logo_data = db.Column(LargeBinary, nullable=True)
    logo_filename = db.Column(db.String(100), nullable=True)
    logo_mime_type = db.Column(db.String(50), nullable=True)
    photo_data = db.Column(LargeBinary, nullable=True)
    photo_filename = db.Column(db.String(100), nullable=True)
    photo_mime_type = db.Column(db.String(50), nullable=True)
    agents = db.relationship('Agent', backref='user_agent', lazy=True, overlaps="user")
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))

    user_roles = db.Table('user_roles',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
        db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
    )
    


    def __init__(self, first_name, last_name, email, business_name, otp=None, is_verified=False,  company_id=None, user_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.otp = otp
        self.is_verified = is_verified
        self.business_name = business_name
        self.user_id = user_id
        self.company_id = company_id

    




class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    otp = db.Column(db.String(4), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    time = db.Column(db.String(10), default=datetime.now().strftime("%H:%M:%S"))
    email = db.Column(db.String(120), unique=True, nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'))
    street_1 = db.Column(db.String(100))
    street_2 = db.Column(db.String(100))
    town_city = db.Column(db.String(50))
    state_province = db.Column(db.String(50))
    post_code = db.Column(db.String(50))
    country = db.Column(db.String(50))
    business_phone = db.Column(db.String(20))
    business_email = db.Column(db.String(120))
    website = db.Column(db.String(100))
    photo_data = db.Column(LargeBinary, nullable=True)
    photo_filename = db.Column(db.String(100), nullable=True)
    photo_mime_type = db.Column(db.String(50), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_agent_user_id'), nullable=False)
    trading_name = db.Column(db.String(50))
    logo_data = db.Column(LargeBinary, nullable=True)
    logo_filename = db.Column(db.String(100), nullable=True)
    logo_mime_type = db.Column(db.String(50), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_agent_user_id'), nullable=False)
    user = db.relationship('User', back_populates='agents', overlaps="user_agent")  # Adjust overlaps parameter


    
    pcc_code_prefix = 'CMB'

    pcc_code_sequence = db.Sequence('pcc_code_sequence')
    

    # Define pcc_code_prefix as a class attribute
    

    def __init__(self, first_name, last_name, email, otp, business_name=None , agent_business_name =None):
        super().__init__(first_name=first_name, last_name=last_name, email=email, otp=otp, business_name=business_name)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.otp = otp
        self.business_name = business_name

        self.agent_business_name = agent_business_name

    @validates('pcc_code_counter')
    def validate_pcc_code_counter(self, key, value):
        if value is None:
            return 0
        return value
    

    def generate_pcc_code(self):
        if not self.pcc_code:
            highest_pcc_code = Agent.query.with_entities(func.max(Agent.pcc_code)).scalar()
            if highest_pcc_code:
                prefix, counter = highest_pcc_code.split('-')
                next_counter = int(counter) + 1
                new_pcc_code = f"{prefix}-{next_counter:04d}"
            else:
                # If no existing records, start from 'CMB-0001'
                new_pcc_code = 'CMB-0001'

            self.pcc_code = new_pcc_code

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_id = db.Column(db.String(10), nullable=False)
    full_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone_no = db.Column(db.String(20), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    is_leads = db.Column(db.Boolean, default=False)
    lead_type = db.Column(db.String(50), nullable=True)
    marketing_type = db.Column(db.String(50), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('customers', lazy=True))
    __table_args__ = (db.UniqueConstraint('customer_id', 'company_id', name='_customer_company_uc'),)


    def __init__(self, full_name, email, phone_no, company_id, user_id, customer_id=None,
                 is_verified=False, is_leads=False, lead_type=None, marketing_type=None):
        self.full_name = full_name
        self.email = email
        self.phone_no = phone_no
        self.company_id = company_id
        self.user_id = user_id
        self.customer_id = customer_id
        self.is_verified = is_verified
        self.is_leads = is_leads
        self.lead_type = lead_type
        self.marketing_type = marketing_type


 

class CustomerComment(db.Model):
    __tablename__ = 'customer_comments'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.String(10), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lead_id = db.Column(db.String(10), db.ForeignKey('leads.lead_id'), nullable=False)  # Link to the Leads table
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', foreign_keys=[created_by], backref=db.backref('customer_comments', lazy='dynamic'))


class Lead(db.Model):
    __tablename__ = 'leads'
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.String(10), nullable=False)
    company_id = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id') , nullable=False)
    customer_id = db.Column(db.String(10), db.ForeignKey('customer.customer_id', ondelete='SET NULL'), nullable=True)
    is_leads = db.Column(db.Integer, default=1)  # Default to 1 for 'In Progress'
    lead_type = db.Column(db.String(50), nullable=True)
    marketing_type = db.Column(db.String(50), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    customer = db.relationship('Customer', foreign_keys=[customer_id], backref='leads')
    user = db.relationship('User', backref='leads')
    inquiry_type = db.Column(db.String(50), nullable=True)  # Add this line in your Lead model
 

    @staticmethod
    def generate_lead_id(company_id):
        last_lead = Lead.query.filter_by(company_id=company_id).order_by(Lead.id.desc()).first()
        if last_lead:
            last_number = int(last_lead.lead_id[2:])  # Assuming the lead_id format is "LDXXXXX"
            new_id = f'LD{last_number + 1:05d}'
        else:
            new_id = 'LD00001'
        return new_id



   

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    permissions = db.relationship('Permission', secondary='role_permissions', backref=db.backref('roles', lazy='dynamic'))

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

role_permissions = db.Table('role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'), primary_key=True)
)





    












												




