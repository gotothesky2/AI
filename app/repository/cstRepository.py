from app.domain.Cst import Cst
from .Repository import BaseRepository

class CstRepository(BaseRepository[Cst]):
    def __init__(self):
        super().__init__(model=Cst)


cstRepository = CstRepository()
