from flask_sqlalchemy import SQLAlchemy
from .extensions import db

class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    max_votes = db.Column(db.Integer, default=1)
    options = db.relationship('Option', backref='poll', lazy=True)

class Voter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    votes = db.relationship('Vote', backref='option', lazy=True)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voter_name = db.Column(db.String(80), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('option.id'), nullable=False)
