from repository import Repository, BaseRepository
from domain.report import Report

class ReportRepository(BaseRepository[Report]):
    def __init__(self):
        super().__init__(model=Report)

reportRepository = ReportRepository()
