from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email, ValidationError, Optional
from application.models import Winners

class WinForm(FlaskForm):
	name = StringField('Name',
		validators=[
			DataRequired(),
			Length(min=2, max=30)
			])	
	email = StringField('Email',
		validators=[
			Optional(),
			Email()
		])
	mobile = IntegerField('Mobile Number',
		validators=[
			Optional()
		])
	submit = SubmitField('WIN!!!')
