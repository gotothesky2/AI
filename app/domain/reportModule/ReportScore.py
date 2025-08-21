from sqlalchemy.dialects.mysql import DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger,VARBINARY
from ..entity import BaseEntity
from decimal import Decimal

class ReportScore(BaseEntity):
    __tablename__ = 'report_score'
    __table_args__ = {
        'extend_existing': True,
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    id=Column(BigInteger,name='rs_id',primary_key=True)
    subject=Column(String(50),name='subject',nullable=False)#세부 과목명
    grade=Column(Integer,name='grade',nullable=True) #등급
    studentNum=Column(Integer,name='student_num',nullable=True) #학생 수
    standardDeviation=Column(VARBINARY(50),name='standard_deviation',nullable=True) #표준편차
    subjectAverage=Column(Integer,name='subject_average',nullable=True) #과목 평균
    achievement=Column(String,name='achievement',nullable=True) #성취도
    score=Column(Integer,name='score',nullable=True) #원점수
    credit=Column(Integer,name='credit',nullable=False) #학점

    rId=Column(BigInteger,ForeignKey('report.r_id'),name='r_id',nullable=False)

    report=relationship("Report", back_populates="reportScores")

    def getStandardDeviation(self) -> Decimal:
        return Decimal(self.standardDeviation.decode('utf-8')) if self.standardDeviation else None

    def setStandardDeviation(self,value):
        self.standardDeviation=str(round(float(value),1)).encode('utf-8') if value else None