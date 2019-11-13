from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = '7218a9143c27c16610765205a1b21cb7'

from application import routes
