from flask import render_template, redirect, url_for, request
from application import app
from application.forms import WinForm
from application.letter_gen import Letter_gen
from application.num_gen import Number_gen
from application.prize_gen import Prize_gen
from random import shuffle

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
	form = WinForm()

	if form.validate_on_submit():
		temp2 = (Letter_gen() + str(Number_gen()))
		char_list = list(temp2)
		shuffle(char_list)
		temp2 = ''.join(char_list)
		
		
		lists = send_data(form.name.data, temp2, form.email.data, 
				  form.mobile.data, Prize_gen())
		print (lists)
		
	return render_template('home.html', title='Home', form=form)

def send_data(name, acc, ema, mob, prize):
	output = []
	
	output.append(name)
	output.append(acc)
	output.append(ema)
	output.append(mob)
	output.append(prize)
	
	return output
