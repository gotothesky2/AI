from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CstResponse(BaseModel):
    id: int
    uid: str
    pdfLink: str
    cstGradeNum: int
    cstTermNum: int
    uploadTime: datetime
    mathScore: float
    spaceScore: float
    creativeScore: float
    natureScore: float
    artScore: float
    musicScore: float
    langScore: float
    selfScore: float
    handScore: float
    relationScore: float
    physicalScore: float

    model_config = ConfigDict(from_attributes=True)