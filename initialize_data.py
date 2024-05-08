from app import db
from init_db import Role

def initialize_roles():
    roles = ['Admin', 'Supervisor', 'User']
    existing_roles = Role.query.with_entities(Role.name).all()
    existing_roles = [r[0] for r in existing_roles]  # Convert list of tuples to list of strings
    for role_name in roles:
        if role_name not in existing_roles:
            new_role = Role(name=role_name)
            db.session.add(new_role)
    db.session.commit()

