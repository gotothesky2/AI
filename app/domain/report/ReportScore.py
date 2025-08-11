from sqlalchemy.dialects.mysql import DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger,VARBINARY
from domain.entity import BaseEntity
from decimal import Decimal

class ReportScore(BaseEntity):
    __tablename__ = 'report_score'
    __table_args__ = {
        'extend_existing': True,
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    id=Column(BigInteger,name='rs_id',primary_key=True)
    subject=Column(String(50),name='subject',nullable=False)
    grade=Column(Integer,name='grade',nullable=True)
    studentNum=Column(Integer,name='student_num',nullable=True)
    _standardDeviation=Column(VARBINARY(50),name='standard_deviation',nullable=True)
    subjectAverage=Column(Integer,name='subject_average',nullable=True)
    achievement=Column(String,name='achievement',nullable=True)
    score=Column(Integer,name='score',nullable=True)
    credit=Column(Integer,name='credit',nullable=False)

    rId=Column(BigInteger,ForeignKey('report.r_id'),name='r_id',nullable=False)

    report=relationship("Report", back_populates="reportScores")

    def getStandardDeviation(self) -> Decimal:
        return Decimal(self._standardDeviation.decode('utf-8'))

    def setStandardDeviation(self,value):
        self._standardDeviation=str(round(float(value),1)).encode('utf-8') if value else None