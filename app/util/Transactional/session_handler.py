from contextlib import contextmanager
from app.db import SessionLocal
from sqlalchemy.orm import Session

@contextmanager
def transactional_session():
    db: Session = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()