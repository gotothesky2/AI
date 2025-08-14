from domain.Field import Field
from .Repository import BaseRepository
from typing import Optional, List

class FieldRepository(BaseRepository[Field]):
    def __init__(self):
        super().__init__(model=Field)
    
    def getByName(self, name: str) -> Optional[Field]:
        """학문 분야명으로 학문 분야를 조회합니다."""
        return (self.session.query(self.model)
                .filter(self.model.name == name)
                .first())
    
    def searchByName(self, name: str) -> List[Field]:
        """학문 분야명에 특정 문자열이 포함된 학문 분야들을 조회합니다."""
        return (self.session.query(self.model)
                .filter(self.model.name.contains(name))
                .all())
    
    def getAllOrderedByName(self) -> List[Field]:
        """학문 분야명 순으로 정렬된 모든 학문 분야를 조회합니다."""
        return (self.session.query(self.model)
                .order_by(self.model.name)
                .all())


fieldRepository = FieldRepository()
