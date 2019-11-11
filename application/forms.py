from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from application.models import Winners

class WinForm(FlaskForm):
	name = StringField('Name',
		validators=[
			DataRequired(),
			Length(min=2, max=30)
			])	
	email = StringField('Email',
		validators=[
			Email()
		])
	mobile = IntegerField('Mobile Number')
	submit = SubmitField('Login')
