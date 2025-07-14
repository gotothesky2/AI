from fastapi import UploadFile

from app.repository.userRepository import UserRepository
from app.util.PdfExtracter.HmtExtracter import HmtExtracter
from app.util.Transactional import Transactional
from app.repository.hmtRepository import hmtRepository, HmtRepository
from app.repository.userRepository import userRepository,UserRepository
from app.domain.Hmt import Hmt
import uuid
from app.domain.User import User
from datetime import datetime
from app.DTO.HmtDTO import HmtResponse

class HmtService:
    def __init__(self,hmtRepository: HmtRepository,userRepository: UserRepository):
        self._hmtRepository= hmtRepository
        self._userRepository = userRepository
        self._s3=None

    #흥미검사 첨부 기능
    @Transactional
    def createHmt(self, user_id:str ,file:UploadFile):
        user:User=self._userRepository.getById(user_id)
        scores=HmtExtracter(file)
        pdf_bytes = file.file.read()
        key=f"hmt/{user.uid}/{uuid.uuid4().hex}.pdf"
        pdf_url = self._s3.upload_bytes(pdf_bytes, key)

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


        return newHmt

    @Transactional
    def deleteHmt(self,hmtId:int):
        removeObj=self._hmtRepository.getById(hmtId)
        if removeObj is None:
            raise Exception(f"Hmt with id {hmtId} not found")
        self._hmtRepository.remove(removeObj)
    @Transactional
    def getHmtById(self,hmtId:int):
        getObj=self._hmtRepository.getById(hmtId)
        if getObj is None:
            raise Exception(f"Hmt with id {hmtId} not found")
        return getObj

    @Transactional
    def allHmtByUserId(self,user_id:str):
        user:User=self._userRepository.getById(user_id)
        if user is None:
            raise Exception(f"Hmt with id {user_id} not found")
        allHmt=user.hmts
        if allHmt is None:
            raise Exception(f"Hmt with id {user_id} not found")
        return [ HmtResponse.model_validate(c, from_attributes=True)
        for c in allHmt ]

hmtService = HmtService(hmtRepository,userRepository)

