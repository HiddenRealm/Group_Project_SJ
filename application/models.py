from application import db
from flask_login import UserMixin
from datetime import datetime

class Winners(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), nullable=False)
	account = db.Column(db.String(30), nullable=False)
	email = db.Column(db.String(30), nullable=True)
	mobile_number = db.Column(db.Integer, nullable=True)
	prize = db.Column(db.Integer, nullable=False)
