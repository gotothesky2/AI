from functools import wraps
from app.util.Transactional.session_handler import transactional_session

def Transactional(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        with transactional_session() as db:
            return fn(*args, db=db, **kwargs)
    return wrapper