from db import SessionLocal
from util.globalDB.db_context import set_db, reset_db
from functools import wraps


def Transactional(fn):
    """쓰기 작업을 위한 트랜잭션 데코레이터"""
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


def TransactionalRead(fn):
    """읽기 전용 작업을 위한 트랜잭션 데코레이터 (커밋하지 않음)"""
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        session = SessionLocal()
        token = set_db(session)
        try:
            result = fn(self, *args, **kwargs)
            return result
        except Exception:
            session.rollback()
            raise
        finally:
            reset_db(token)
            session.close()
    return wrapper


def TransactionalWrite(fn):
    """쓰기 작업을 위한 트랜잭션 데코레이터 (명시적 커밋)"""
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