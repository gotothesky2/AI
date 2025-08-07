from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime
from repository.oauthRepository import oauthRepository
from repository.userRepository import userRepository
from domain.User import User

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    token = credentials.credentials

    # 1. OAuth 테이블에서 access_token으로 조회
    oauth_record = oauthRepository.findByAccessToken(token)
    if not oauth_record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰입니다."
        )
    # 2. 만료 확인
    if oauth_record.expireDate < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰이 만료되었습니다."
        )
    # 3. 사용자 정보 조회
    user = userRepository.getById(oauth_record.uid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다."
        )
    return user