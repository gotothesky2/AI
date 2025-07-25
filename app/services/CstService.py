from fastapi import UploadFile

from app.repository.userRepository import userRepository,UserRepository
from app.util.PdfExtracter.CstExtracter import CstExtracter
from app.util.Transactional import Transactional
from app.repository.cstRepository import CstRepository,cstRepository
from app.domain.Cst import Cst
from app.DTO.CstDTO import CstResponse
import uuid
from app.domain.User import User

class CstService:
    def __init__(self,cstRepository: CstRepository,userRepository: UserRepository):
        self._cstRepository = cstRepository
        self._userRepository = userRepository
        self._s3=None

    @Transactional
    def createCst(self,user_id:str,file:UploadFile):
        user=self._userRepository.getById(user_id)
        if user is None:
            raise Exception(f"User {user_id} not found")
        
        # PDF 추출 먼저 수행
        scores=CstExtracter(file)
        
        # 파일 포인터를 처음으로 되돌린 후 S3 업로드용 바이트 읽기
        file.file.seek(0)
        pdf_bytes = file.file.read()
        key = f"cst/{user.uid}/{uuid.uuid4().hex}.pdf"
        pdf_url = self._s3.upload_bytes(pdf_bytes, key)

        newCst=Cst(
            user=user,
            pdfLink=pdf_url,
            cstGradeNum=user.gradeNum,
            mathScore=scores.get("수리·논리력",-1),
            spaceScore=scores.get("공간지각력",-1),
            creativeScore=scores.get("창의력",-1),
            natureScore=scores.get("자연친화력",-1),
            artScore=scores.get("예술시각능력",-1),
            musicScore=scores.get("음악능력",-1),
            langScore=scores.get("언어능력",-1),
            selfScore=scores.get("자기성찰능력",-1),
            handScore=scores.get("손재능",-1),
            relationScore=scores.get("대인관계능력",-1),
            physicalScore=scores.get("신체·운동능력",-1)
        )
        self._cstRepository.save(newCst)
        
        # JPA처럼 심플하게 - @Transactional이 알아서 flush 처리
        return CstResponse.model_validate(newCst, from_attributes=True)

    @Transactional
    def deleteCst(self,cstId:int):
        removeObj=self._cstRepository.getById(cstId)
        if removeObj is None:
            raise Exception(f"Cst {cstId} not found")
        self._cstRepository.remove(removeObj)

    @Transactional
    def getCstById(self,cstId:int):
        getObj=self._cstRepository.getById(cstId)
        if getObj is None:
            raise Exception(f"Cst {cstId} not found")
        return getObj
    @Transactional
    def allCstByUser(self,user_id:str):
        user:User=self._userRepository.getById(user_id)
        if user is None:
            raise Exception(f"User {user_id} not found")
        allCsts=user.csts
        if allCsts is None:
            raise Exception(f"Cst {user.uid} not found")
        return [CstResponse.model_validate(c,from_attributes=True) for c in allCsts]

cstService = CstService(cstRepository,userRepository)

