
from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Flask-WTF requires an encryption key - the string can be anything'

# Flask-Bootstrap requires this line
Bootstrap(app)
