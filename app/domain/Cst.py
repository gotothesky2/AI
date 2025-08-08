from sqlalchemy.orm import relationship
from .entity.BaseEntity import BaseEntity
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, BigInteger
from datetime import datetime
from util.termGenerator import default_term

class Cst(BaseEntity):
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

    user = relationship('User', back_populates="csts")

