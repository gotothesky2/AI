from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from repository.userRepository import userRepository
from domain.User import User
from .jwt_auth import get_current_user as jwt_get_current_user, verify_token_only

security = HTTPBearer()

# JWT 기반 인증으로 교체
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """JWT를 사용한 현재 사용자 인증 (자바 백엔드에서 생성된 JWT 토큰 검증)"""
    return await jwt_get_current_user(credentials)

def verify_token(token: str) -> dict:
    """JWT 토큰만 검증 (자바 백엔드용)"""
    return verify_token_only(token)