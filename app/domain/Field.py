from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, BigInteger

from domain.entity import BaseEntity


class Field(BaseEntity):
    __table_args__ = {
        'extend_existing': True,
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }
    id=Column(BigInteger,name='f_id',primary_key=True)
    name=Column(String,name='f_name',nullable=False)

    majors=relationship("Major", back_populates="field")

