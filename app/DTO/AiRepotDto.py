from pydantic import BaseModel,ConfigDict, Field, field_validator
from datetime import datetime
from typing import Optional, Any

class AiReportListResponse(BaseModel):
    id: int
    reportGradeNum: int
    reportTermNum: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class AiReportResponse(BaseModel):
    id: int
    reportGradeNum: int
    reportTermNum:int
    userName:Optional[str]=None
    created_at:datetime
    CstID:int
    HmtID:int
    testReport:Optional[str]=None
    scoreReport:Optional[str]=None
    majorReport:Optional[str]=None
    totalReport:Optional[str]=None

    model_config = ConfigDict(from_attributes=True)
    
    @field_validator('userName', mode='before')
    @classmethod
    def get_user_name(cls, v, info):
        """AiReport 객체에서 user.name을 추출합니다."""
        if hasattr(info.data, 'user') and info.data.user:
            return getattr(info.data.user, 'name', None)
        return v

class AiReportRequest(BaseModel):
    reportGradeNum: int=Field(description='레포트 생성할 학년(반영 성적 및 추천 내용 달라짐)')
    reportTermNum: int=Field(description='레포트 생성할 학기(반영 성적 및 추천 내용 달라짐)')
