from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime

class CstRead(BaseModel):
    id: int
    user_id: int            = Field(..., alias="userId")
    pdf_link: str       = Field(..., alias="pdfLink")
    cst_grade_num: int      = Field(..., alias="cstGradeNum")
    cst_term_num: int       = Field(..., alias="cstTermNum")
    cst_score: float        = Field(..., alias="cstScore")
    upload_time: datetime   = Field(..., alias="uploadTime")
    math_score: float       = Field(..., alias="mathScore")
    space_score: float      = Field(..., alias="spaceScore")
    creative_score: float   = Field(..., alias="creativeScore")
    nature_score: float     = Field(..., alias="natureScore")
    art_score: float        = Field(..., alias="artScore")
    music_score: float      = Field(..., alias="musicScore")
    lang_score: float       = Field(..., alias="langScore")
    self_score: float       = Field(..., alias="selfScore")
    hand_score: float       = Field(..., alias="handScore")
    relation_score: float   = Field(..., alias="relationScore")
    physical_score: float   = Field(..., alias="physicalScore")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": 1,
                "userId": 123,
                "pdfLink": "https://s3.amazonaws.com/bucket/cst/123/report.pdf",
                "cstGradeNum": 2,
                "cstTermNum": 1,
                "cstScore": 85.5,
                "uploadTime": "2025-07-12T10:15:30",
                "mathScore": 90.0,
                "spaceScore": 80.0,
                "creativeScore": 75.0,
                "natureScore": 88.0,
                "artScore": 70.0,
                "musicScore": 95.0,
                "langScore": 85.0,
                "selfScore": 80.0,
                "handScore": 90.0,
                "relationScore": 85.0,
                "physicalScore": 78.0
            }
        }
