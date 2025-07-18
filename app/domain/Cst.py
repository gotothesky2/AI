from sqlalchemy.orm import relationship
from .entity.BaseEntity import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, BigInteger
from datetime import datetime

def default_term() -> int:
    """현재 월이 1~6월이면 1학기, 7~12월이면 2학기 반환"""
    month = datetime.now().month
    return 1 if month < 7 else 2

class Cst(Base):
    __tablename__ = 'cst'
    __table_args__ = {'extend_existing': True}
    
    # 실제 DB 컬럼명에 맞춰 매핑 (DB명 != Python명)
    id = Column(BigInteger, name='at_id', primary_key=True, autoincrement=True, nullable=False)
    uid = Column(String(36), ForeignKey("user.uid"), name='uid', nullable=False)
    pdfLink = Column(String(255), name='pdf_link', nullable=False)
    cstGradeNum = Column(Integer, name='cst_grade_num', nullable=False)
    cstTermNum = Column(Integer, name='cst_term_num', nullable=False, default=default_term)
    uploadTime = Column(DateTime, name='upload_time', default=datetime.now, nullable=False)
    mathScore = Column(Float, name='math_score', nullable=False)
    spaceScore = Column(Float, name='space_score', nullable=False)
    creativeScore = Column(Float, name='creative_score', nullable=False)
    natureScore = Column(Float, name='nature_score', nullable=False)
    artScore = Column(Float, name='art_score', nullable=False)
    musicScore = Column(Float, name='music_score', nullable=False)
    langScore = Column(Float, name='lang_score', nullable=False)
    selfScore = Column(Float, name='self_score', nullable=False)
    handScore = Column(Float, name='hand_score', nullable=False)
    relationScore = Column(Float, name='relation_score', nullable=False)
    physicalScore = Column(Float, name='physical_score', nullable=False)
    createdAt = Column(DateTime, name='created_at', nullable=True)
    updatedAt = Column(DateTime, name='updated_at', nullable=True)

    user = relationship('User', back_populates="csts")

