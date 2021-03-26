from datetime import datetime
from sound.app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(50),unique=False, nullable=False)
	lastname = db.Column(db.String(50),unique=False, nullable=False)
	password = db.Column(db.String(50), nullable=False)
	token_id = db.Column(db.String)
	emailid = db.Column(db.String(100),unique=True, nullable=False)
	templates = db.relationship('Template', backref='user', lazy=True)

class Template(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	subject = db.Column(db.String(50), nullable=False)
	body = db.Column(db.String(120), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)