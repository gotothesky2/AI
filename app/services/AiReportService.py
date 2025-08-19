from domain import User
from domain import AiReport
from repository.userRepository import userRepository
from repository.mockRepository import mockRepository
from repository.mockScoreRepository import mockScoreRepository
from repository.cstRepository import cstRepository
from repository.hmtRepository import hmtRepository
from repository.aiReportRepository import aiReportRepository
from repository.reportRepository import reportRepository
from DTO.AiRepotDto import AiReportResponse, AiReportListResponse, AiReportRequest
from gptApi import *
from util.Transactional import Transactional,TransactionalRead
from domain.AiReport import AiReport
from domain.User import User
from DTO.AiRepotDto import AiReportResponse,AiReportListResponse
from services.UserService import userService
from enum import Enum



from util.termGenerator import default_term
from globals import (
    ErrorCode,
    raise_business_exception,
    raise_database_exception,
    raise_file_exception,
    BusinessException,
    FileException,
    DatabaseException
)

class AiReportTokenCost(Enum):
    COST_OF_BEFOR_SECOND=30
    COST_OF_BEFOR_THIRD=50
    COST_OF_AFTER_THIRD=70



class AiReportService:
    def __init__(self):
        self._cstRepository = cstRepository
        self._hmtRepository = hmtRepository
        self._userRepository = userRepository
        self._mockRepository = mockRepository
        self._mockScoreRepository = mockScoreRepository
        self._aiReportRepository = aiReportRepository
        self._reportRepository = reportRepository
        self._userService = userService



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
            if request.reportGradeNum > 1:
                reports = self._reportRepository.getSortReportByUid(user_id)
                
                # 필요한 모든 학년-학기 조합 확인
                required_reports = set()
                for grade in range(1, request.reportGradeNum):
                    for term in range(1, 3):
                        required_reports.add((grade, term))

                required_reports.add((request.reportGradeNum,1))
                required_reports.add((request.reportGradeNum, request.reportTermNum))

                
                # 실제 존재하는 레포트 확인
                existing_reports = set()
                for report in reports:
                    existing_reports.add((report.userGrade, report.term))
                
                # 누락된 레포트 확인
                missing_reports = required_reports - existing_reports
                
                if missing_reports:
                    missing_list = [f"{grade}학년 {term}학기" for grade, term in sorted(missing_reports)]
                    raise BusinessException(
                        ErrorCode.AI_REPORT_NOT_VALID_GRADE_TERM,
                        f"AI 리포트 생성을 위해 다음 성적 레포트가 필요합니다: {', '.join(missing_list)}"
                    )



            cost=0

            if len(required_reports)<=2:#test 레포트만
                cost=AiReportTokenCost.COST_OF_BEFOR_SECOND
            if len(required_reports)<4: #성적레포트까지
                cost=AiReportTokenCost.COST_OF_BEFOR_THIRD
            if len(required_reports)>=4:#관심 학교 학과 까지
                cost=AiReportTokenCost.COST_OF_AFTER_THIRD

            aiTestContent = TestReport(hmt=userHmt, cst=userCst)
            aiGradeContent=None
            aiMajorContent=None
            aiTotalContent=None

            if cost >= AiReportTokenCost.COST_OF_BEFOR_THIRD:
                aiGradeContent=GptScoreReport(user)
            if cost >= AiReportTokenCost.COST_OF_AFTER_THIRD:
                pass
            aiReport=AiReport(user=user,
                              reportTermNum=request.reportTermNum,
                              reportGradeNum=request.reportGradeNum,
                              testReport=aiTestContent,
                              majorContent=aiMajorContent,
                              scoreReport=aiGradeContent,
                              totalReport=aiTotalContent,
                              hmtID=userHmt,
                              cstID=userCst)
            self._userService.deductTokenForService(uid=user.uid,service_name="aiReport",token_cost=cost)
            self._aiReportRepository.save(aiReport)
            return AiReportResponse.model_validate(aiReport,from_attributes=True)
        except BusinessException:
            raise
        except Exception as e:
            raise DatabaseException(
                ErrorCode.DATABASE_ERROR,
                f"AI 리포트 생성 중 오류가 발생했습니다: {str(e)}"
            )




AiReportService=AiReportService()
