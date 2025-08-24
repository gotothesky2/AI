from domain.MajorBookmark import MajorBookmark
from .Repository import BaseRepository
from typing import Optional, List
from sqlalchemy.orm import joinedload

class MajorBookmarkRepository(BaseRepository[MajorBookmark]):
    def __init__(self):
        super().__init__(model=MajorBookmark)
    
    def getByUserId(self, uid: str) -> List[MajorBookmark]:
        """사용자 ID로 북마크된 학과-학교 목록을 조회합니다."""
        return (self.session.query(self.model)
                .options(joinedload(self.model.major), joinedload(self.model.university))
                .filter(self.model.uid == uid)
                .all())
    
    def getByUserIdWithUniversityAndMajor(self, uid: str) -> List[MajorBookmark]:
        """사용자 ID로 대학교와 학과 정보가 모두 있는 북마크만 조회합니다."""
        return (self.session.query(self.model)
                .options(joinedload(self.model.major), joinedload(self.model.university))
                .filter(self.model.uid == uid)
                .filter(self.model.univId.isnot(None))
                .filter(self.model.major_id.isnot(None))
                .all())

majorBookmarkRepository = MajorBookmarkRepository()
