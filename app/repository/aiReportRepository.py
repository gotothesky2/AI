from domain.AiReport import AiReport
from .Repository import BaseRepository
from typing import Optional

class AiReportRepository(BaseRepository[AiReport]):
    def __init__(self):
        super().__init__(model=AiReport)


aiReportRepository = AiReportRepository()