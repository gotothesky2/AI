from sqlalchemy.orm import Session, joinedload
from app.domain.Cst import Cst

class CstRepository:
    def __init__(self, db: Session):
        self.db=db
    def create(self,obj:Cst):
        self.db.add(obj)
        return obj
    def getById(self,id:int)->Cst | None:
        return self.db.query(Cst).filter(Cst.id==id).first()
    def deleteById(self,id:int):
        obj=self.getById(id)
        if obj:
            self.db.delete(obj)
            return True
        raise Exception(f"Hmt with id {id} not found")

