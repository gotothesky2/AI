from domain.UniversityMajor import UniversityMajor
from .Repository import BaseRepository
from typing import List

class UniversityMajorRepository(BaseRepository[UniversityMajor]):
    def __init__(self):
        super().__init__(model=UniversityMajor)
    
    def getByUniversityId(self, universityId: int) -> List[UniversityMajor]:
        """특정 대학에 개설된 전공들을 조회합니다."""
        return (self.session.query(self.model)
                .filter(self.model.univId == universityId)
                .all())
    
    def getByMajorId(self, majorId: int) -> List[UniversityMajor]:
        """특정 전공이 개설된 대학들을 조회합니다."""
        return (self.session.query(self.model)
                .filter(self.model.mId == majorId)
                .all())
    
    def getByUniversityAndMajor(self, universityId: int, majorId: int) -> UniversityMajor:
        """특정 대학의 특정 전공 정보를 조회합니다."""
        return (self.session.query(self.model)
                .filter(self.model.univId == universityId)
                .filter(self.model.mId == majorId)
                .first())


universityMajorRepository = UniversityMajorRepository()
