
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

# import csv
# from app import db
# from app.models import Carrier

# def import_carriers_from_csv(data):
#     carriers = []
#     reader = csv.DictReader(data.splitlines())
#     for row in reader:
#         carrier = Carrier(
#             name=row['name'],
#             email=row['email'],
#             phone=row['phone'],
#             company=row['company'],
#             address=row['address'],
#             allowed_items=row['allowed_items'].split(','),  # Assuming the CSV contains a comma-separated list
#             max_load_quantity=int(row['max_load_quantity'])
#         )
#         carriers.append(carrier)
#     db.session.bulk_save_objects(carriers)
#     db.session.commit()

