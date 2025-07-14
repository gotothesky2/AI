from app.domain.User import User
from app.repository.Repository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=User)

userRepository = UserRepository()
