from sqlite3 import *
from flask import Flask, render_template
from . import db


app = Flask(__name__)
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')
