
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from redis import Redis
from rq import Queue

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object('app.config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

redis_conn = Redis(host='redis', port=6379)
task_queue = Queue(connection=redis_conn)

from app import routes, models

# old code
# # Trying a simple connection
# from config import db, app
# from models import *

# with app.app_context():
#     db.drop_all()
#     db.create_all()
#     print("Tables created successfully!")


# sqlachademy code. Change after
# from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/tms'
# db = SQLAlchemy(app)

# from . import routes

# def create_app():
#     db.create_all()
#     return app

