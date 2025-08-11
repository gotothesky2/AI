from sqlalchemy.orm import relationship
from .entity.BaseEntity import BaseEntity
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger,Text
from datetime import datetime
from util.termGenerator import default_term

class AiReport(BaseEntity):
    __tablename__='ai_report'
    id = Column(BigInteger,name='ai_report_id', primary_key=True,autoincrement=True,nullable=False)
    uid = Column(String(36), ForeignKey("user.uid"), name='uid', nullable=False)
    testReport = Column(Text,name='test_report', nullable=True)
    scoreReport = Column(Text,name='score_report', nullable=True)
    majorReport = Column(Text,name='major_report', nullable=True)
    totalReport = Column(Text,name='total_report', nullable=True)
    reportGradeNum=Column(Integer,name='report_grade_num', nullable=False, default=default_term)
    reportTermNum=Column(Integer,name='report_term_num', nullable=False, default=default_term)

    user = relationship("User", back_populates="aiReports")