from flask import render_template, redirect, url_for, request
from application import app
from application.forms import WinForm
import boto3
import json

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
	form = WinForm()
	temp3 = ''

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

		random.invoke(FunctionName='PushDataToQueue',
						Payload=json.dumps(package))

		print(package['mobile'])

		if package['email'] == '':
			print("1")
			if package['mobile'] == 'None':
				print("2")
				temp3 = "You have won " + package['prize'] + " well played."
				print(temp3)

	return render_template('home.html', title='Home', form=form, prize=temp3)

def send_data(name, acc, ema, mob, prize):
	output = { "account":acc, "name":name, "email":ema, "mobile":str(mob), "prize":prize}
	return output