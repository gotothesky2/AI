from domain.report.ReportScore import ReportScore
from .Repository import BaseRepository
from typing import List

class ReportScoreRepository(BaseRepository[ReportScore]):
    def __init__(self):
        super().__init__(model=ReportScore)
    
    def getByReportId(self, reportId: int) -> List[ReportScore]:
        """특정 리포트의 모든 점수를 조회합니다."""
        return (self.session.query(self.model)
                .filter(self.model.rId == reportId)
                .all())
    
    def getBySubject(self, reportId: int, subject: str) -> ReportScore:
        """특정 리포트의 특정 과목 점수를 조회합니다."""
        return (self.session.query(self.model)
                .filter(self.model.rId == reportId)
                .filter(self.model.subject == subject)
                .first())
    
    def getByCategory(self, reportId: int, category: int) -> List[ReportScore]:
        """특정 리포트의 특정 카테고리 점수들을 조회합니다."""
        return (self.session.query(self.model)
                .filter(self.model.rId == reportId)
                .filter(self.model.category == category)
                .all())


reportScoreRepository = ReportScoreRepository()
