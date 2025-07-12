from fastapi import UploadFile
from app.util.PdfExtracter.HmtExtracter import HmtExtracter
from app.util.Transactional import Transactional
from app.repository.hmtRepository import hmtRepository, HmtRepository
from app.domain.Hmt import Hmt
from app.domain.User import User
from datetime import datetime
from app.DTO.HmtDTO import HmtResponse

class HmtService:
    def __init__(self,hmtRepository: HmtRepository):
        self._hmtRepository= hmtRepository

    #흥미검사 첨부 기능
    @Transactional
    def createHmt(self,user:User,file:UploadFile):
        scores=HmtExtracter(file)
        pdf_url="test"
        newHmt=Hmt(
            user=user,
            hmtGradeNum=user.gradeNum,
            pdfLink=pdf_url,
            rScore=scores.get("R",-1),
            iScore=scores.get("I",-1),
            aScore=scores.get("A",-1),
            sScore=scores.get("S",-1),
            eScore=scores.get("E",-1),
            cScore=scores.get("C",-1)
        )
        self._hmtRepository.save(newHmt)
        return HmtResponse.model_validate(newHmt)
    @Transactional
    def deleteHmt(self,hmtId:int):
        removeObj=self._hmtRepository.getById(hmtId)
        if removeObj is None:
            raise Exception(f"Hmt with id {hmtId} not found")
        self._hmtRepository.remove(removeObj)
    @Transactional
    def getHmtById(self,hmtId:int):
        if hmtId is None:
            raise Exception(f"Hmt with id {hmtId} not found")
        return HmtResponse.model_validate(self._hmtRepository.getById(hmtId))


