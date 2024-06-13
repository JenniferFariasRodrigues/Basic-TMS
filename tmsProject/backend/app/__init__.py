
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

