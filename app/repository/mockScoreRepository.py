from domain.mock.MockScore import MockScore
from .Repository import BaseRepository
from typing import List

class MockScoreRepository(BaseRepository[MockScore]):
    def __init__(self):
        super().__init__(model=MockScore)
    
    def getByMockId(self, mockId: int) -> List[MockScore]:
        """특정 모의고사의 모든 점수를 조회합니다."""
        return (self.session.query(self.model)
                .filter(self.model.mockId == mockId)
                .all())
    
    def getByCategory(self, mockId: int, category: int) -> MockScore:
        """특정 모의고사의 특정 카테고리 점수를 조회합니다."""
        return (self.session.query(self.model)
                .filter(self.model.mockId == mockId)
                .filter(self.model.category == category)
                .first())
    
    def getBySubjectName(self, mockId: int, name: str) -> MockScore:
        """특정 모의고사의 특정 과목명 점수를 조회합니다."""
        return (self.session.query(self.model)
                .filter(self.model.mockId == mockId)
                .filter(self.model.name == name)
                .first())


mockScoreRepository = MockScoreRepository()
