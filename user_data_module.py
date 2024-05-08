from init_db import User, Agent


def fetch_user_data(email):
    # Fetch user data based on the email
    user = User.query.filter_by(email=email).first()
    return user




def fetch_agent_data(email):
    # Fetch agent data based on the email
    agent = Agent.query.filter_by(email=email).first()
    return agent

def fetch_related_agent(user):
    # Assuming User has a relationship with Agent using agent_id
    if user:
        return Agent.query.get(user.agent_id)
    return None





def fetch_agent_by_id(agent_id):
    return Agent.query.get(agent_id)

def fetch_user_by_id(user_id):
    return User.query.get(user_id)






   
