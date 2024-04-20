'''
db
database file, containing all the logic to interface with the sql database
'''
import hashlib
import secrets
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import *

from pathlib import Path

# creates the database directory
Path("database") \
    .mkdir(exist_ok=True)

# "database/main.db" specifies the database file
# change it if you wish
# turn echo = True to display the sql output
engine = create_engine("sqlite:///database/main.db", echo=False)

# initializes the database
Base.metadata.create_all(engine)

# inserts a user to the database
def insert_user(username: str, password: str):
    salt = generate_salt()
    hashed_password = hash_password(password, salt)
    with Session(engine) as session:
        user = User(username=username, password=hashed_password, salt=salt)
        session.add(user)
        session.commit()

# gets a user from the database
def get_user(username: str):
    with Session(engine) as session:
        return session.query(User).filter_by(username=username).first()
    
# generate salt
def generate_salt():
    return secrets.token_hex(16)

# hash and salt the password
def hash_password(password: str, salt: str):
    return hashlib.sha256((password + salt).encode()).hexdigest()

# verify the password
def verify_password(password: str, hashed_password: str, salt: str):
    return hashed_password == hash_password(password, salt)

# show the user's friend list
def get_friends(username: str):
    with Session(engine) as session:
        user = session.query(User).filter_by(username=username).first()
        if user:
            return user.friends
    return []
    
