from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, BigInteger, ForeignKey,Integer

from domain.entity import BaseEntity


class Major(BaseEntity):
    __table_args__ = {
        'extend_existing': True,
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }
    id = Column(BigInteger, name='m_id', primary_key=True)
    name = Column(String, name='m_name', nullable=False)
    fId = Column(BigInteger, ForeignKey('field.f_id'),name='f_id',nullable=False)
    code=Column(Integer, name='m_code',nullable=False)


    universitys = relationship("University", secondary='university_major', viewonly=True)
