from app.domain.Hmt import Hmt
from .Repository import BaseRepository

class HmtRepository(BaseRepository[Hmt]):
    def __init__(self):
        super().__init__(Hmt)


hmtRepository = HmtRepository()
