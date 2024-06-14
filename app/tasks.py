from celery import Celery
from flask import current_app as app
import csv
from .models import db, Carrier
def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)

@celery.task
def process_csv(data):
    csv_data = csv.DictReader(data.splitlines())
    for row in csv_data:
        carrier = Carrier.query.filter_by(email=row['email']).first()
        if carrier:
            for key, value in row.items():
                setattr(carrier, key, value)
        else:
            carrier = Carrier(**row)
            db.session.add(carrier)
    db.session.commit()
    return {'status': 'completed'}
