from domain.Hmt import Hmt
from .Repository import BaseRepository
from typing import Optional

class HmtRepository(BaseRepository[Hmt]):
    def __init__(self):
        super().__init__(model=Hmt)
    
    def getLatestByUserId(self, user_id: str) -> Optional[Hmt]:
        """사용자의 가장 최신 HMT를 조회합니다."""
        return (self.session.query(self.model)
                .filter(self.model.uid == user_id)
                .order_by(self.model.uploadTime.desc())
                .first())


hmtRepository = HmtRepository()
