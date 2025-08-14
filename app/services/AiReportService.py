from domain import User
from repository.userRepository import userRepository
from repository.mockRepository import mockRepository
from repository.mockScoreRepository import mockScoreRepository
from repository.cstRepository import cstRepository
from repository.hmtRepository import hmtRepository
from repository.aiReportRepository import aiReportRepository
from DTO.AiRepotDto import AiReportResponse, AiReportListResponse, AiReportRequest
from gptApi.testReportEng import testReport

from util.Transactional import Transactional
from domain.AiReport import AiReport
from domain.User import User
from DTO.AiRepotDto import AiReportResponse,AiReportListResponse

from globals import (
    ErrorCode,
    raise_business_exception,
    raise_database_exception,
    raise_file_exception,
    BusinessException,
    FileException,
    DatabaseException
)

class AiReportService:
    def __init__(self):
        self._cstRepository = cstRepository
        self._hmtRepository = hmtRepository
        self._userRepository = userRepository
        self._mockRepository = mockRepository
        self._mockScoreRepository = mockScoreRepository
        self._aiReportRepository = aiReportRepository

    @Transactional
    def getAiReportsByUser(self,user_id:str):
        try:
            user:User=self._userRepository.getUserById(user_id)
            if user is None:
                raise BusinessException(ErrorCode.USER_NOT_FOUND,f"User  not found")
            userAiReports=user.aiReports
            result=[]
            for aiReport in userAiReports:
                reportDto=AiReportListResponse.model_validate(aiReport,from_attributes=True)
                reportDto.userName=user.name
                result.append(reportDto)
            return result
        except Exception as e:
            raise e

    @Transactional
    def getAireportByID(self,aiReportId:int):
        try:
            report=self._aiReportRepository.getAiReportById(aiReportId)
            if report is None:
                raise BusinessException(ErrorCode.AI_REPORT_NOT_FOUND,f"AI Report with Id not found")
            reportResult=AiReportResponse.model_validate(report,from_attributes=True)
            reportResult.userName=report.user.name
            return reportResult
        except Exception as e:
            raise e

    @Transactional
    def createAiReport(self,request:AiReportRequest,user_id:str):
        try:
            if (not 0<request.reportGradeNum<=3) or (not 0<request.reportTermNum<=2):
                raise BusinessException(ErrorCode.AI_REPORT_NOT_VALID_GRADE_TERM,f"부적절한 학년 학기입니다. 요청하실 학년 학기를 다시 입력해 주세요")
            user=self._userRepository.getUserById(user_id)
            if user is None:
                raise BusinessException(ErrorCode.USER_NOT_FOUND,f"User not found")
            userHmt=self._hmtRepository.getUserHmtById(user_id)
            if userHmt is None:
                raise BusinessException(ErrorCode.HMT_NOT_FOUND,f"직업 흥미검사를 실시해주세요.")
            userCst=self._cstRepository.getUserCstById(user_id)
            if userCst is None:
                raise BusinessException(ErrorCode.CST_NOT_FOUND,f"직업 적성검사를 실시해 주세요.")
            if request.reportGradeNum>1:
                for 