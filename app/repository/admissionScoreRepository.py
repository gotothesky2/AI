from repository.Repository import BaseRepository
from domain.AdmissionScore import AdmissionScore
from typing import List, Optional

class AdmissionScoreRepository(BaseRepository[AdmissionScore]):
    def __init__(self):
        super().__init__(AdmissionScore)
    
    def getByUniversityAndMajor(self, univId: int, majorId: int) -> Optional[AdmissionScore]:
        """특정 대학교-학과의 입학 성적 데이터를 조회합니다."""
        return self.session.query(AdmissionScore).filter(
            AdmissionScore.univId == univId,
            AdmissionScore.majorId == majorId
        ).first()
    
    def getByUniversityId(self, univId: int) -> List[AdmissionScore]:
        """특정 대학교의 모든 입학 성적 데이터를 조회합니다."""
        return self.session.query(AdmissionScore).filter(
            AdmissionScore.univId == univId
        ).all()
    
    def getByMajorId(self, majorId: int) -> List[AdmissionScore]:
        """특정 학과의 모든 입학 성적 데이터를 조회합니다."""
        return self.session.query(AdmissionScore).filter(
            AdmissionScore.majorId == majorId
        ).all()
    
    def updateOrCreate(self, univId: int, majorId: int, **score_data) -> AdmissionScore:
        """입학 성적 데이터를 업데이트하거나 생성합니다."""
        existing = self.getByUniversityAndMajor(univId, majorId)
        
        if existing:
            # 기존 데이터 업데이트
            for key, value in score_data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            return existing
        else:
            # 새 데이터 생성
            new_score = AdmissionScore(
                univId=univId,
                majorId=majorId,
                **score_data
            )
            self.save(new_score)
            return new_score

admissionScoreRepository = AdmissionScoreRepository()
