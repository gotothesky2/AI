from domain.University import University
from .Repository import BaseRepository
from typing import Optional, List

class UniversityRepository(BaseRepository[University]):
    def __init__(self):
        super().__init__(model=University)
    
    def getByName(self, name: str) -> Optional[University]:
        """대학명으로 대학을 조회합니다."""
        return (self.session.query(self.model)
                .filter(self.model.name == name)
                .first())
    
    def searchByName(self, name: str) -> List[University]:
        """대학명에 특정 문자열이 포함된 대학들을 조회합니다."""
        return (self.session.query(self.model)
                .filter(self.model.name.contains(name))
                .all())
    
    def getAllOrderedByName(self) -> List[University]:
        """대학명 순으로 정렬된 모든 대학을 조회합니다."""
        return (self.session.query(self.model)
                .order_by(self.model.name)
                .all())


universityRepository = UniversityRepository()
