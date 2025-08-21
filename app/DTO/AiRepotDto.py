from pydantic import BaseModel,ConfigDict, Field, field_validator
from datetime import datetime
from typing import Optional, Any
import json

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
    testReport:Optional[dict]=None
    scoreReport:Optional[dict]=None
    majorReport:Optional[dict]=None
    totalReport:Optional[dict]=None

    model_config = ConfigDict(from_attributes=True)
    
    @field_validator('userName', mode='before')
    @classmethod
    def get_user_name(cls, v, info):
        """AiReport 객체에서 user.name을 추출합니다."""
        if hasattr(info.data, 'user') and info.data.user:
            return getattr(info.data.user, 'name', None)
        return v

    @field_validator('testReport', mode='before')
    @classmethod
    def parse_test_report(cls, v, info):
        """testReport 문자열을 JSON으로 파싱합니다."""
        if isinstance(v, str):
            # 'None' 문자열이나 빈 문자열은 None으로 처리
            if v.lower() in ['none', 'null', ''] or v.strip() == '':
                return None
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return v
        return v

    @field_validator('scoreReport', mode='before')
    @classmethod
    def parse_score_report(cls, v, info):
        """scoreReport 문자열을 JSON으로 파싱합니다."""
        if isinstance(v, str):
            # 'None' 문자열이나 빈 문자열은 None으로 처리
            if v.lower() in ['none', 'null', ''] or v.strip() == '':
                return None
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return v
        return v

    @field_validator('majorReport', mode='before')
    @classmethod
    def parse_major_report(cls, v, info):
        """majorReport 문자열을 JSON으로 파싱합니다."""
        if isinstance(v, str):
            # 'None' 문자열이나 빈 문자열은 None으로 처리
            if v.lower() in ['none', 'null', ''] or v.strip() == '':
                return None
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return v
        return v

    @field_validator('totalReport', mode='before')
    @classmethod
    def parse_total_report(cls, v, info):
        """totalReport 문자열을 JSON으로 파싱합니다."""
        if isinstance(v, str):
            # 'None' 문자열이나 빈 문자열은 None으로 처리
            if v.lower() in ['none', 'null', ''] or v.strip() == '':
                return None
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return v
        return v

class AiReportRequest(BaseModel):
    reportGradeNum: int=Field(description='레포트 생성할 학년(반영 성적 및 추천 내용 달라짐)')
    reportTermNum: int=Field(description='레포트 생성할 학기(반영 성적 및 추천 내용 달라짐)')
