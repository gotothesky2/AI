from domain.entity import BaseEntity
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger,DECIMAL
from sqlalchemy.orm import relationship
from enum import Enum
class CategoryName(Enum):
    KOREAN=0
    MATH=1
    ENGLISH=2
    KHISTORY=3
    SOCIAL=4
    SCIENCE=5


class Report(BaseEntity):
    __tablename__ = 'report'
    __table_args__ = {
        'extend_existing': True,
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4 '
    }
    id=Column(BigInteger,name='r_id',primary_key=True)
    categoryName :CategoryName = Column(Integer,name='category_name',nullable=False)#과목 카테고리
    categoryGrade=Column(DECIMAL(5,2),name='category_grade',nullable=True)#과목 등급
    uid=Column(String,ForeignKey('user.uid'),name='uid',nullable=False)#유저 아이디
    term=Column(Integer,name='term',nullable=False)#학기
    userGrade=Column(Integer,name='user_grade',nullable=False)#유저 학년

    user=relationship("User",back_populates="reports")
    reportScores=relationship("ReportScore",back_populates="report")
