from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, BigInteger
from sqlalchemy.orm import relationship
from .entity.BaseEntity import BaseEntity
from datetime import datetime

def default_term() -> int:
    """현재 월이 1~6월이면 1학기, 7~12월이면 2학기 반환"""
    month = datetime.now().month
    return 1 if month < 7 else 2

class Hmt(BaseEntity):
    id=Column(BigInteger, primary_key=True, autoincrement=True)
    uid=Column(String,ForeignKey('user.uid'),nullable=False)#java에 스트링으로 대있어서 그렇게함
    pdfLink=Column(String,nullable=False)
    hmtGradeNum=Column(Integer,nullable=False)
    hmtTermNum=Column(Integer,nullable=False,default=default_term)
    uploadTime=Column(DateTime,nullable=False,default=datetime.now)
    rScore=Column(Float,nullable=False)
    iScore=Column(Float,nullable=False)
    aScore=Column(Float,nullable=False)
    sScore=Column(Float,nullable=False)
    eScore=Column(Float,nullable=False)
    cScore=Column(Float,nullable=False)

    user=relationship("User",back_populates="hmts")



