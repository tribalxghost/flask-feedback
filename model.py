from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(
        db.String,primary_key=True,unique=True,nullable = False
    )
    password = db.Column(
        db.String, nullable = False
    )
    email = db.Column(
        db.String,unique = True,nullable=False
    )
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String, nullable = False)
   

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique = True, autoincrement = True)
    title = db.Column(db.String(0,100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    username = db.Column(db.String, db.ForeignKey('users.username'))
    user = db.relationship("User", backref=db.backref("users", cascade="all,delete"))
