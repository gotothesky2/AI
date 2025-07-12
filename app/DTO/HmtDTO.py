from pydantic import BaseModel, Field
from datetime import datetime

class HmtResponse(BaseModel):
    id: int
    uid: str            = Field(..., alias="uid")
    rScore: float       = Field(..., alias="rScore")
    iScore: float       = Field(..., alias="iScore")
    aScore: float       = Field(..., alias="aScore")
    sScore: float       = Field(..., alias="sScore")
    eScore: float       = Field(..., alias="eScore")
    cScore: float       = Field(..., alias="cScore")
    pdfLink: str        = Field(..., alias="pdfLink")
    uploadTime: datetime = Field(..., alias="uploadTime")
    hmtTermNum: int     = Field(..., alias="hmtTermNum")
    hmtGradeNum: int    = Field(..., alias="hmtGradeNum")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": 1,
                "uid": "user123",
                "rScore": 4.5,
                "iScore": 3.2,
                "aScore": 5.0,
                "sScore": 2.7,
                "eScore": 4.8,
                "cScore": 3.9,
                "pdfLink": "https://your-bucket.s3.amazonaws.com/hmt/user123/report.pdf",
                "uploadTime": "2025-07-12T10:15:30",
                "hmtTermNum": 1,
                "hmtGradeNum": 2
            }
        }