# app/models.py
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db
from flask_login import UserMixin
from app import login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # User model: Contains information for each user, including their id, username, and hashed password.
    def __repr__(self):
        return '<User {}>'.format(self.username)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Chat model: Contains information about individual chats, including the id, user id, timestamp, context, and completion status.
class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.String(20), nullable=False)
    context = db.Column(db.Text, nullable=False)
    is_complete = db.Column(db.Boolean, nullable=False)

# Message model: Contains information about individual messages in chats, including the id, chat id, user id, timestamp, text, and response status.
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    timestamp = db.Column(db.String(20), nullable=False)
    text = db.Column(db.Text, nullable=False)
    is_response = db.Column(db.Boolean, nullable=False)
