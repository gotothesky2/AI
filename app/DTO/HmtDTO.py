from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from app.domain.Hmt import Hmt
class HmtResponse(BaseModel):
    rScore: float
    iScore: float
    aScore: float
    sScore: float
    eScore: float
    cScore: float
    pdfLink: str
    uploadTime: datetime
    hmtTermNum: int
    hmtGradeNum: int

    model_config = ConfigDict(from_attributes=True)

