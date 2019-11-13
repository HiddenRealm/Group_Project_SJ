from flask import render_template, redirect, url_for, request
from application import app, db
from application.models import Winners
from application.forms import WinForm
from application.letter_gen import Letter_gen
from application.num_gen import Number_gen
from application.prize_gen import Prize_gen

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
	form = WinForm()

	if form.validate_on_submit():
		temp2 = (Letter_gen() + str(Number_gen()))
		temp = Winners(
			name=form.name.data,
			account=temp2,
			email=form.email.data,
			mobile_number=form.mobile.data,
			prize=Prize_gen())
		db.session.add(temp)
		db.session.commit()
		if not form.email.data and not form.mobile.data:
			print("Hi")
	return render_template('home.html', title='Home', form=form)