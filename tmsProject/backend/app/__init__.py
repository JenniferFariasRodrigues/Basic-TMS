from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/tms'
db = SQLAlchemy(app)

from . import routes

def create_app():
    db.create_all()
    return app

