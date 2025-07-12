from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, BigInteger
from sqlalchemy.orm import relationship
from .entity.BaseEntity import BaseEntity
from datetime import datetime

class Hmt(BaseEntity):
    id=Column(BigInteger, primary_key=True, autoincrement=True)
    uid=Column(String,ForeignKey('user.uid'),nullable=False)#java에 스트링으로 대있어서 그렇게함
    pdfLink=Column(String,nullable=False)
    hmtGradeNum=Column(Integer,nullable=False)
    hmtTermNum=Column(Integer,nullable=False)
    uploadTime=Column(DateTime,nullable=False,default=datetime.now())
    rScore=Column(Float,nullable=False)
    iScore=Column(Float,nullable=False)
    aScore=Column(Float,nullable=False)
    sScore=Column(Float,nullable=False)
    eScore=Column(Float,nullable=False)
    cScore=Column(Float,nullable=False)

    user=relationship("User",back_populates="hmts")



