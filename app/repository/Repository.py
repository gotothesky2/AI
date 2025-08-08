from typing import TypeVar, Generic, Type, List, Optional, Union
from sqlalchemy.orm import Session
from util.globalDB.global_db import get_global_db # db_context를 통해 가져오는 세션

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    @property
    def session(self) -> Session:
        return get_global_db()

    def save(self, entity: T, flush_immediately: bool = True) -> T:
        """엔티티를 저장합니다. flush_immediately가 False이면 즉시 flush하지 않습니다."""
        self.session.add(entity)
        if flush_immediately:
            self.session.flush()  # 즉시 DB 동기화
        return entity

    def save_all(self, entities: List[T]) -> List[T]:
        """여러 엔티티를 배치로 저장합니다."""
        self.session.add_all(entities)
        self.session.flush()
        return entities

    def getById(self, id: Union[int, str]) -> Optional[T]:
        """ID로 엔티티 조회 (int 또는 string 지원)"""
        return self.session.get(self.model, id)

    def getAll(self) -> List[T]:
        return self.session.query(self.model).all()

    def remove(self, entity: T) -> None:
        self.session.delete(entity)

    def commit(self) -> None:
        """현재 트랜잭션을 커밋합니다."""
        self.session.commit()

    def rollback(self) -> None:
        """현재 트랜잭션을 롤백합니다."""
        self.session.rollback()

    def flush(self) -> None:
        """현재 세션의 변경사항을 데이터베이스에 동기화합니다."""
        self.session.flush()