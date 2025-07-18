from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, BigInteger
from sqlalchemy.orm import relationship
from .entity.BaseEntity import BaseEntity
from datetime import datetime


def default_term() -> int:
    """현재 월이 1~6월이면 1학기, 7~12월이면 2학기 반환"""
    month = datetime.now().month
    return 1 if month < 7 else 2

class Hmt(BaseEntity):
    __tablename__ = 'hmt'
    __table_args__ = {'extend_existing': True}
    
    # 실제 DB 컬럼명에 맞춰 매핑 (DB명 != Python명)
    id = Column(BigInteger, name='it_id', primary_key=True, autoincrement=True)
    uid = Column(String(36), ForeignKey('user.uid'), name='uid', nullable=False)
    pdfLink = Column(String(255), name='pdf_link', nullable=False)
    hmtGradeNum = Column(Integer, name='hmt_grade_num', nullable=False)
    hmtTermNum = Column(Integer, name='hmt_term_num', nullable=False, default=default_term)
    uploadTime = Column(DateTime, name='upload_time', nullable=False, default=datetime.now)
    rScore = Column(Float, name='r_score', nullable=False)
    iScore = Column(Float, name='i_score', nullable=False)
    aScore = Column(Float, name='a_score', nullable=False)
    sScore = Column(Float, name='s_score', nullable=False)
    eScore = Column(Float, name='e_score', nullable=False)
    cScore = Column(Float, name='c_score', nullable=False)

    user = relationship("User", back_populates="hmts")



