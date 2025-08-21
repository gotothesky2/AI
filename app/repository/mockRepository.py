from repository.Repository import  BaseRepository
from domain.mockModule.Mock import Mock

class MockRepository(BaseRepository[Mock]):
    def __init__(self):
        super().__init__(model=Mock)
mockRepository = MockRepository()