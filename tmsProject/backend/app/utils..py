import re

def validate_carrier(data):
    if len(data) != 5:
        return False
    name, email, phone, company, address = data
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    if not re.match(r"\d{10}", phone):
        return False
    if not company:
        return False
    return True
