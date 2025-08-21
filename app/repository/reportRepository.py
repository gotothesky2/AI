from repository import Repository, BaseRepository
from domain.reportModule import Report

class ReportRepository(BaseRepository[Report]):
    def __init__(self):
        super().__init__(model=Report)

    def getSortReportByUid(self, user_id):
        return (self.session.query(self.model)
                .filter(self.model.uid == user_id)
                .order_by(self.model.userGrade, self.model.term))
reportRepository = ReportRepository()
