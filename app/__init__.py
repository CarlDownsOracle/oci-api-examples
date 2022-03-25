
from flask import Flask
from flask_bootstrap import Bootstrap

flask_app = Flask(__name__)

flask_app.config['SECRET_KEY'] = 'Flask-WTF requires an encryption key - the string can be anything'

# Flask-Bootstrap requires this line
Bootstrap(flask_app)
