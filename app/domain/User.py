# app/domain/user.py
from sqlalchemy import Column, String, Integer, DateTime, Enum
from sqlalchemy.orm import relationship
from .entity.BaseEntity import Base

class User(Base):
    __tablename__ = 'user'
    __table_args__ = {
        'extend_existing': True,
        # 기존 테이블 구조 그대로 사용
        'mysql_engine': 'InnoDB',  # Spring 기본 엔진과 일치
        'mysql_charset': 'utf8mb4'  # Spring 기본 charset과 일치
    }

    # Spring 테이블의 Primary Key만 정의
    uid = Column(String(36), primary_key=True)
    
    # 자주 사용하는 컬럼들만 명시적으로 매핑 (DB명 != Python명)
    name = Column(String(40), name='name', nullable=True)
    email = Column(String(50), name='email', nullable=True) 
    phoneNumber = Column(String(20), name='phone_number', nullable=True)
    gradeNum = Column(Integer, name='grade_num', nullable=True)
    highschool = Column(String(40), name='highschool', nullable=True)
    sex = Column(String(50), name='sex', nullable=True)  # ENUM
    token = Column(Integer, name='token', nullable=False)
    createdAt = Column(DateTime, name='created_at', nullable=True)
    updatedAt = Column(DateTime, name='updated_at', nullable=True)
    
    # Python 전용 관계 (실제 테이블에는 없는 논리적 관계)
    hmts = relationship('Hmt', back_populates='user')
    csts = relationship('Cst', back_populates='user')
    
    def __repr__(self):
        return f"<User(uid='{self.uid}', name='{getattr(self, 'name', None)}')>"