from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    email = db.Column(db.String(40), unique=True)
    phoneNumber = db.Column(db.String(255), unique=True)
    hash_password = db.Column(db.String(80))
    salt = db.Column(db.String(80))
    open_id = db.Column(db.String(50))
    account_type = db.Column(db.Integer)
    add_time = db.Column(db.TEXT)

    def __init__(self, username,hash_password,salt,email,account_type,status):
        self.username = username
        self.hash_password = hash_password
        self.salt = salt
        self.email = email
        self.account_type = account_type
        self.status = status
        self.add_time = datetime.now()
