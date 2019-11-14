from flask import render_template, redirect, url_for, request
from application import app
from application.forms import WinForm
import boto3
import json

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
	form = WinForm()

	if form.validate_on_submit():
		random = boto3.client('lambda')

		account = random.invoke(FunctionName='AccountCreation',
								InvocationType='RequestResponse')

		prize = random.invoke(FunctionName='PrizeGen',
								InvocationType='RequestResponse')

		temp = json.loads(prize['Payload'].read().decode("utf-8"))
		temp2 = json.loads(account['Payload'].read().decode("utf-8"))
		
		package = send_data(form.name.data, temp2, form.email.data, 
				  form.mobile.data, temp)

		random.invoke(FunctionName='PushingData',
						Payload=json.dumps(package))

	return render_template('home.html', title='Home', form=form)

def send_data(name, acc, ema, mob, prize):
	output = { "account":acc, "name":name, "email":ema, "mobile":str(mob), "prize":prize}
	return output