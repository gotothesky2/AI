from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,BigInteger,DECIMAL
from sqlalchemy.orm import relationship
from ..entity.BaseEntity import Base

class MockScore(Base):
    __tablename__ = "mock_score"
    __table_args__ ={
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'extend_existing': True
    }

    id = Column(BigInteger,name='ms_id', primary_key=True)
    mockId=Column(BigInteger,ForeignKey('mock.mock_id'),name='mock_id',nullable=False)
    createAt=Column(DateTime,name="create_at",nullable=True)#생성일
    updateAt=Column(DateTime,name="update_at",nullable=True)#수정일
    cumulative=Column(DECIMAL(5,2),name="cumulative",nullable=True)#누적점수
    category=Column(Integer,name="category",nullable=False)#카테고리
    grade=Column(Integer,name="grade",nullable=False) #등급
    name=Column(String(255),name="name",nullable=True) #과목명
    percetile=Column(Integer,name="percetile",nullable=True) #백분위
    standardScore=Column(Integer,name="standard_score",nullable=True) #표준점수

    mock=relationship("Mock", back_populates="mockScores")



