from contextvars import ContextVar
from sqlalchemy.orm import Session

_db_ctx: ContextVar[Session] = ContextVar("db_ctx")

def set_db(session: Session):
    return _db_ctx.set(session)

def reset_db(token):
    _db_ctx.reset(token)

def get_db() -> Session:
    return _db_ctx.get()