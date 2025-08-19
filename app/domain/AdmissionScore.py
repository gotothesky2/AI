from sqlalchemy.orm import relationship
from sqlalchemy import Column, BigInteger, String, Integer, Float, ForeignKey
from .entity.BaseEntity import BaseEntity

class AdmissionScore(BaseEntity):
    __tablename__ = 'admission_score'
    __table_args__ = {
        'extend_existing': True,
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }
    
    id = Column(BigInteger, name='score_id', primary_key=True, autoincrement=True)
    
    # univ_major와 1대1 연결 (복합 외래키)
    univId = Column(BigInteger, name='univ_id', nullable=False)
    majorId = Column(BigInteger, name='major_id', nullable=False)
    
    # 성적 데이터 컬럼들
    admissionType = Column(String(100), name='admission_type', nullable=False)  # 교과성적우수자전형
    cutFifty = Column(Float, name='cut_fifty', nullable=True)
    cutSeventy = Column(Float, name='cut_seventy', nullable=True)
    cutNinety = Column(Float, name='cut_ninety', nullable=True)
    
    # univ_major와의 관계 (1대1)
    university_major = relationship("UniversityMajor", 
                                 foreign_keys=[univId, majorId],
                                 primaryjoin="and_(AdmissionScore.univId==UniversityMajor.univId, "
                                            "AdmissionScore.majorId==UniversityMajor.mId)")
    
    def __repr__(self):
        return f"<AdmissionScore(univ_id={self.univId}, major_id={self.majorId}, type={self.admissionType})>"
