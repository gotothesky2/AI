from . import User
from .entity.BaseEntity import Base
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey,BigInteger
from sqlalchemy.orm import relationship

class OAuth(Base):
    __tablename__ = 'oauth'
    __table_args__ = {
        'extend_existing': True,
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    id=Column(BigInteger, primary_key=True)
    providerUserId=Column(String(255),name='provider_user_id', nullable=False)
    accessToken=Column(String(255),name='access_token', nullable=False)
    expireDate=Column(DateTime,name='expire_date', nullable=False)
    provider=Column(String(20),name='provider', nullable=False)
    uid=Column(String(36),ForeignKey('user.uid',ondelete='CASCADE'),name='id', nullable=False)

    user=relationship('User', back_populates='auth')
