# from .models import db, Carrier
# from .utils import validate_carrier
# from rq import get_current_job

# # Function to process CSV file content asynchronously
# def process_csv(file_content):
#     job = get_current_job()
#     lines = file_content.split('\n')
#     for line in lines:
#         if line.strip():
#             data = line.split(',')
#             if validate_carrier(data):
#                 name, email, phone, company, address = data
#                 carrier = Carrier.query.filter_by(email=email).first()
#                 if carrier:
#                     carrier.name = name
#                     carrier.phone = phone
#                     carrier.company = company
#                     carrier.address = address
#                 else:
#                     carrier = Carrier(name=name, email=email, phone=phone, company=company, address=address)
#                     db.session.add(carrier)
#             else:
#                 # Log ou manejar dados inválidos
#                 pass
#     db.session.commit()
#     job.meta['progress'] = 100
#     job.save_meta()
