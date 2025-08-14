from sqlalchemy import Column, Integer,BigInteger,ForeignKey,String,DateTime
from sqlalchemy.orm import relationship
from ..entity.BaseEntity import Base

class Mock(Base):
    __tablename__ = "mock"
    __table_args__ = {
        'extend_existing': True,
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }
    id=Column(BigInteger,name='mock_id',primary_key=True)
    uid=Column(String(36),ForeignKey('user.uid'),name='uid',nullable=False)
    examYear=Column(Integer,name="exam_year",nullable=False)
    examMonth=Column(Integer,name="exam_month",nullable=False)
    examGrade=Column(Integer,name="exam_grade",nullable=False)
    createAt=Column(DateTime,name="create_at",nullable=False)
    updateAt=Column(DateTime,name="update_at",nullable=False)

    user=relationship("User",back_populates="mocks")
    mockScores=relationship("MockScore",back_populates="mock")

