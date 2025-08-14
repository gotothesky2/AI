from pydantic import BaseModel,ConfigDict, Field
from datetime import datetime
from typing import Optional

class AiReportListResponse(BaseModel):
    id: int
    reportGradeNum: int
    reportTermNum: int
    userName: Optional[str]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class AiReportResponse(BaseModel):
    id: int
    reportGradeNum: int
    reportTermNum:int
    userName:Optional[str]=None
    created_at:datetime
    CstID:int
    HmtId:int
    testReport:Optional[str]=None
    scoreReport:Optional[str]=None
    majorReport:Optional[str]=None
    totalReport:Optional[str]=None

    model_config = ConfigDict(from_attributes=True)

class AiReportRequest(BaseModel):
    reportGradeNum: int=Field(description='레포트 생성할 학년(반영 성적 및 추천 내용 달라짐)')
    reportTermNum: int=Field(description='레포트 생성할 학기(반영 성적 및 추천 내용 달라짐)')
