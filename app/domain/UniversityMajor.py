from sqlalchemy.orm import relationship
from sqlalchemy import Column, BigInteger, ForeignKey

from domain.entity import Base


class UniversityMajor(Base):
    __tablename__='university_major'
    __table_args__ = {
        'extend_existing': True,
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }
    univId = Column(BigInteger,ForeignKey('university.univ_id'), name='univ_id', primary_key=True)
    mId=Column(BigInteger,ForeignKey('major.m_id'), name='m_id', primary_key=True)

    university=relationship("University", back_populates="university_major")
    major=relationship("Major", back_populates="university_major")
