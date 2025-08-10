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
    mock_id=Column(BigInteger,ForeignKey('mock.id'),nullable=False)
    createAt=Column(DateTime,name="create_at",nullable=True)
    updateAt=Column(DateTime,name="update_at",nullable=True)
    cumulative=Column(DECIMAL(5,2),name="cumulative",nullable=True)
    category=Column(Integer,name="category",nullable=False)
    grade=Column(Integer,name="grade",nullable=False)
    name=Column(String(255),name="name",nullable=True)
    percetile=Column(Integer,name="percetile",nullable=True)
    standardScore=Column(Integer,name="standard_score",nullable=True)

    mock=relationship("Mock", back_populates="mocks")



