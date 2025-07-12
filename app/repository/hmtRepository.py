from sqlalchemy.orm import Session, joinedload
from app.domain.Hmt import Hmt
class HmtRepository:
    def __init__(self, db: Session):
        self.db=db
    def create(self,obj:Hmt):
        self.db.add(obj)
        return obj
    def getById(self,id:int)->Hmt | None:
        return self.db.query(Hmt).filter(Hmt.id==id).first()
    def deleteById(self,id:int):
        obj=self.getById(id)
        if obj:
            self.db.delete(obj)
            return True
        raise Exception(f"Hmt with id {id} not found")

