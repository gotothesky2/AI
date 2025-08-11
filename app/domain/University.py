from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, BigInteger,Integer,ForeignKey

from domain.entity import BaseEntity


class University(BaseEntity):
    __table_args__ = {
        'extend_existing': True,
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }
    id = Column(BigInteger, name='univ_id', primary_key=True)
    name = Column(String, name='univ_name', nullable=False)


    majors = relationship("Major",secondary='university_major',viewonly=True)
    university_major=relationship('UniversityMajor', back_populates="university")


