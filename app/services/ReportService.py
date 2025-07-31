from domain.Cst import Cst
from domain.Hmt import Hmt
from domain.User import User
from repository.userRepository import userRepository, UserRepository
from repository.hmtRepository import hmtRepository, HmtRepository
from repository.cstRepository import cstRepository, CstRepository
from gptApi.testReportEng.testReport import testReport
from util.Transactional import Transactional

class ReportService:
    def __init__(self, userRepository:UserRepository, hmtRepository:HmtRepository, cstRepository:CstRepository):
        self.userRepository = userRepository
        self.hmtRepository = hmtRepository
        self.cstRepository = cstRepository

    @Transactional
    def createReport(self, user_id: str):
        # 유저 존재 여부 확인
        user = userRepository.getById(user_id)
        if not user:
            raise ValueError(f"사용자 {user_id}를 찾을 수 없습니다.")
        
        # 가장 최신의 CST를 효율적으로 조회
        cst = cstRepository.getLatestByUserId(user_id)
        if not cst:
            raise ValueError(f"사용자 {user_id}에게 CST 데이터가 없습니다.")
        hmt=hmtRepository.getLatestByUserId(user_id)
        if not hmt:
            raise ValueError(f"사용자 {user_id}에게 HMT 데이터가 없습니다.")
        
        # 테스트 보고서 생성
        test_report = testReport(cst, hmt)
        




