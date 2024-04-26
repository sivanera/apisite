from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = '12121212'

from app import routes
from app import forms
