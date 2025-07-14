# app/domain/user.py
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from .entity.BaseEntity import Base

class User(Base):
    __tablename__ = 'user'  # 기존 테이블과 이름 일치
    __table_args__ = {'extend_existing': True}  # 이미 존재하는 테이블과 매핑

    uid = Column(String(255), primary_key=True)
    gradeNum = Column(Integer, nullable=False)
    name = Column(String(100), nullable=False)
    # Spring DB 기준 맞춰야 함
    # 필요한 경우 추가 컬럼 정의

    # 관계
    hmts = relationship('Hmt', back_populates='user')
    csts = relationship('Cst', back_populates='user')