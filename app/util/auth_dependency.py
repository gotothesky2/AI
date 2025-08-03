from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from .jwt_util import jwt_util
from repository.userRepository import userRepository
from domain.User import User

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """현재 로그인한 사용자 정보 반환"""
    try:
        # JWT 토큰에서 사용자 ID 추출
        user_id = jwt_util.get_user_id_from_token(credentials.credentials)
        
        # 데이터베이스에서 사용자 정보 조회
        user = userRepository.getById(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="사용자를 찾을 수 없습니다."
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증에 실패했습니다."
        )

async def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """현재 로그인한 사용자 ID만 반환"""
    return jwt_util.get_user_id_from_token(credentials.credentials) 