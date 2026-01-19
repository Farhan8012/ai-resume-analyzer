import json
import os

# The file where we store user data
DB_FILE = "users.json"

def load_users():
    """Loads users from the JSON database."""
    # If file doesn't exist, return empty dictionary
    if not os.path.exists(DB_FILE):
        return {}
    
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_user(email, password, name):
    """Saves a new user to the database."""
    users = load_users()
    
    # Check if user already exists
    if email in users:
        return False 
    
    # Add new user
    users[email] = {
        "password": password,
        "name": name
    }
    
    # Save back to file
    with open(DB_FILE, "w") as f:
        json.dump(users, f)
    return True

def authenticate(email, password):
    """Checks if email/password match."""
    users = load_users()
    if email in users and users[email]["password"] == password:
        return users[email]["name"]
    return None