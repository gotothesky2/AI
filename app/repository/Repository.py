from typing import TypeVar, Generic, Type, List, Optional
from sqlalchemy.orm import Session
from app.util.globalDB.global_db import db  # db_context를 통해 가져오는 세션

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: Session = db):
        self.model = model
        self.session = session

    def save(self, entity: T) -> T:
        self.session.add(entity)
        return entity

    def getById(self, id: int) -> Optional[T]:
        return self.session.get(self.model, id)

    def getAll(self) -> List[T]:
        return self.session.query(self.model).all()

    def remove(self, entity: T) -> None:
        self.session.delete(entity)