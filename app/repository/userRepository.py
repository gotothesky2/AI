from domain.User import User
from repository.Repository import BaseRepository
from typing import Optional

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=User)

userRepository = UserRepository()
