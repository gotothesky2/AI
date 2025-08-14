from domain.Major import Major
from .Repository import BaseRepository
from typing import Optional, List

class MajorRepository(BaseRepository[Major]):
    def __init__(self):
        super().__init__(model=Major)
    
    def getByName(self, name: str) -> Optional[Major]:
        """전공명으로 전공을 조회합니다."""
        return (self.session.query(self.model)
                .filter(self.model.name == name)
                .first())
    
    def getByFieldId(self, fieldId: int) -> List[Major]:
        """특정 학문 분야에 속한 전공들을 조회합니다."""
        return (self.session.query(self.model)
                .filter(self.model.fId == fieldId)
                .all())
    
    def getByCode(self, code: int) -> Optional[Major]:
        """전공 코드로 전공을 조회합니다."""
        return (self.session.query(self.model)
                .filter(self.model.code == code)
                .first())
    
    def searchByName(self, name: str) -> List[Major]:
        """전공명에 특정 문자열이 포함된 전공들을 조회합니다."""
        return (self.session.query(self.model)
                .filter(self.model.name.contains(name))
                .all())


majorRepository = MajorRepository()
