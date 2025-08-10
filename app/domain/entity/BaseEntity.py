from sqlalchemy.ext.declarative import as_declarative, declared_attr
from datetime import datetime
from sqlalchemy import Column, DateTime

@as_declarative()
class Base:
    id: int
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

class BaseEntity(Base):
    __abstract__ = True
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=True)