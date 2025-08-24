from sqlalchemy.orm import relationship
from .entity.BaseEntity import BaseEntity
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger

class MajorBookmark(BaseEntity):
    __tablename__ = "major_bookmark"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",
        "extend_existing": True
    }

    id =Column(Integer,name="mb_id",primary_key=True,autoincrement=True)
    major_id=Column(BigInteger,ForeignKey("major.m_id"),name="m_id",nullable=False)
    uid=Column(String(36),ForeignKey('user.uid'),name="uid",nullable=False)
    univId=Column(BigInteger,ForeignKey('university.univ_id'),name="univ_id",nullable=True)#만약 null이라면 학과 북마크 아니라면 학과-학교 북마크

    user=relationship("User",back_populates="majorBookmarks")
    major=relationship("Major",back_populates="majorBookmarks")
    university=relationship("University",back_populates="majorBookmarks")