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

userService = UserService(userRepository) 