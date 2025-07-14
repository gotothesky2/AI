from .db_context import get_db

def get_global_db():
    return get_db()