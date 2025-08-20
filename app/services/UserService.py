from repository.userRepository import userRepository, UserRepository
from domain.User import User
from util.Transactional import Transactional
from datetime import datetime
import uuid

class UserService:
    def __init__(self, userRepository: UserRepository):
        self._userRepository = userRepository

    @Transactional
    def createUser(self, name: str, email: str, phone_number: str = None, 
                   grade_num: int = None, highschool: str = None, sex: str = None):
        """새로운 사용자를 생성합니다."""
        uid = str(uuid.uuid4())
        new_user = User(
            uid=uid,
            name=name,
            email=email,
            phoneNumber=phone_number,
            gradeNum=grade_num,
            highschool=highschool,
            sex=sex,
            token=0,
            createdAt=datetime.now(),
            updatedAt=datetime.now()
        )
        self._userRepository.save(new_user)
        return new_user

    @Transactional
    def getUserById(self, uid: str):
        """사용자 ID로 사용자를 조회합니다."""
        user = self._userRepository.getById(uid)
        if user is None:
            raise Exception(f"User {uid} not found")
        return user

    @Transactional
    def getUserByEmail(self, email: str):
        """이메일로 사용자를 조회합니다."""
        user = self._userRepository.getByEmail(email)
        if user is None:
            raise Exception(f"User with email {email} not found")
        return user

    @Transactional
    def updateUser(self, uid: str, **kwargs):
        """사용자 정보를 업데이트합니다."""
        user = self.getUserById(uid)
        
        # 업데이트 가능한 필드들
        updateable_fields = ['name', 'email', 'phoneNumber', 'gradeNum', 'highschool', 'sex']
        
        for field, value in kwargs.items():
            if field in updateable_fields and value is not None:
                setattr(user, field, value)
        
        user.updatedAt = datetime.now()
        self._userRepository.save(user)
        return user

    @Transactional
    def deleteUser(self, uid: str):
        """사용자를 삭제합니다."""
        user = self.getUserById(uid)
        self._userRepository.remove(user)

    @Transactional
    def getAllUsers(self):
        """모든 사용자를 조회합니다."""
        return self._userRepository.getAll()

    @Transactional
    def updateToken(self, uid: str, token_amount: int):
        """사용자의 토큰을 업데이트합니다."""
        user = self.getUserById(uid)
        user.token = token_amount
        user.updatedAt = datetime.now()
        self._userRepository.save(user)
        return user

    @Transactional
    def addToken(self, uid: str, token_amount: int):
        """사용자에게 토큰을 추가합니다."""
        user = self.getUserById(uid)
        user.token += token_amount
        user.updatedAt = datetime.now()
        return user

    @Transactional
    def useToken(self, uid: str, token_amount: int):
        """사용자의 토큰을 차감합니다. 토큰이 부족하면 예외를 발생시킵니다."""
        user = self.getUserById(uid)
        
        if user.token < token_amount:
            raise Exception(f"Insufficient tokens. Required: {token_amount}, Available: {user.token}")
        
        user.token -= token_amount
        user.updatedAt = datetime.now()
        return user

    @Transactional
    def checkTokenBalance(self, uid: str):
        """사용자의 토큰 잔액을 확인합니다."""
        user = self.getUserById(uid)
        return user.token

    @Transactional
    def hasEnoughTokens(self, uid: str, required_tokens: int):
        """사용자가 필요한 토큰을 가지고 있는지 확인합니다."""
        user = self.getUserById(uid)
        return user.token >= required_tokens

    @Transactional
    def deductTokenForService(self, uid: str, service_name: str, token_cost: int):
        """특정 서비스 사용을 위해 토큰을 차감합니다."""
        user = self.getUserById(uid)
        
        if user.token < token_cost:
            raise Exception(f"Insufficient tokens for {service_name}. Required: {token_cost}, Available: {user.token}")
        
        user.token -= token_cost
        user.updatedAt = datetime.now()
        
        # 토큰 사용 로그를 반환할 수 있습니다 (실제 구현에서는 별도 테이블에 저장)
        return {
            'user_id': uid,
            'service_name': service_name,
            'token_cost': token_cost,
            'remaining_tokens': user.token,
            'used_at': datetime.now()
        }

    @Transactional
    def refundToken(self, uid: str, token_amount: int, reason: str = "환불"):
        """사용자에게 토큰을 환불합니다."""
        user = self.getUserById(uid)
        user.token += token_amount
        user.updatedAt = datetime.now()
        
        return {
            'user_id': uid,
            'refund_amount': token_amount,
            'reason': reason,
            'total_tokens': user.token,
            'refunded_at': datetime.now()
        }

    @Transactional
    def getTokenUsageStats(self, uid: str):
        """사용자의 토큰 사용 통계를 반환합니다."""
        user = self.getUserById(uid)
        return {
            'user_id': uid,
            'current_tokens': user.token,
            'created_at': user.createdAt,
            'last_updated': user.updatedAt
        }

userService = UserService(userRepository) 