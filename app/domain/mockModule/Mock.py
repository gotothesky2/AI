from sqlalchemy import Column, Integer,BigInteger,ForeignKey,String,DateTime
from sqlalchemy.orm import relationship
from ..entity.BaseEntity import BaseEntity

class Mock(BaseEntity):
    __tablename__ = "mock"
    __table_args__ = {
        'extend_existing': True,
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }
    id=Column(BigInteger,name='mock_id',primary_key=True)
    uid=Column(String(36),ForeignKey('user.uid'),name='uid',nullable=False)
    examYear=Column(Integer,name="exam_year",nullable=False)#응시년도
    examMonth=Column(Integer,name="exam_month",nullable=False)#응시월
    examGrade=Column(Integer,name="exam_grade",nullable=False)#응시학년
    

    user=relationship("User",back_populates="mocks")
    mockScores=relationship("MockScore",back_populates="mock") #과목별 모의고사 점수

