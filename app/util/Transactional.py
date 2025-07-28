from db import SessionLocal
from util.globalDB.db_context import set_db,reset_db
from functools import wraps


def Transactional(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        session = SessionLocal()
        token = set_db(session)
        try:
            result = fn(self, *args, **kwargs)
            session.commit()
            return result
        except Exception:
            session.rollback()
            raise
        finally:
            reset_db(token)
            session.close()
    return wrapper