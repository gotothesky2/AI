from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from domain.Hmt import Hmt
class HmtResponse(BaseModel):
    id:int
    rScore: float
    iScore: float
    aScore: float
    sScore: float
    eScore: float
    cScore: float
    uploadTime: datetime
    hmtTermNum: int
    hmtGradeNum: int
    DownloadUrl: str=None

    model_config = ConfigDict(from_attributes=True)

