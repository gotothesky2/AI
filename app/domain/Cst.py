from sqlalchemy.orm import relationship
from .entity.BaseEntity import BaseEntity
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, BigInteger
from datetime import datetime
def default_term() -> int:
    """현재 월이 1~6월이면 1학기, 7~12월이면 2학기 반환"""
    month = datetime.now().month
    return 1 if month < 7 else 2
class Cst(BaseEntity):
    id=Column(BigInteger,primary_key=True,autoincrement=True,nullable=False)
    uid=Column(ForeignKey("user.uid"),nullable=False)
    pdfLink=Column(String,nullable=False)
    cstGradeNum=Column(Integer,nullable=False)
    cstTermNum=Column(Integer,nullable=False,default=default_term)
    cstScore=Column(Float,nullable=False)
    uploadTime=Column(DateTime,default=datetime.now,nullable=False)
    mathScore=Column(Float,nullable=False)
    spaceScore=Column(Float,nullable=False)
    creativeScore=Column(Float,nullable=False)
    natureScore=Column(Float,nullable=False)
    artScore=Column(Float,nullable=False)
    musicScore=Column(Float,nullable=False)
    langScore=Column(Float,nullable=False)
    selfScore=Column(Float,nullable=False)
    handScore=Column(Float,nullable=False)
    relationScore=Column(Float,nullable=False)
    physicalScore=Column(Float,nullable=False)

    relationship('User',back_populates="csts")

