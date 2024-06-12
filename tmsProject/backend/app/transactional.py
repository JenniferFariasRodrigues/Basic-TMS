from functools import wraps
# from config import db
from app import db



def transactional_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = db.session
        try:
            result = func(*args, **kwargs)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            print(f"Unable to save data in the database: {e}")
            raise

    return wrapper
