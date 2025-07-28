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
        pass




