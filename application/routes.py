from flask import render_template, redirect, url_for, request
from application import app, db, bcrypt
from application.models import Winners
from application.forms import WinForm

@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html', title='Home')
