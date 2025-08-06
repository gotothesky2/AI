from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from login.jwt_util import jwt_util
from domain.User import User
from repository.userRepository import userRepository

# HTTP Bearer 토큰 스키마
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """액세스 토큰으로 현재 로그인된 사용자 정보 반환"""
    try:
        token = credentials.credentials
        payload = jwt_util.verify_token(token)
        user_id = payload.get("uid")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="토큰에 사용자 정보가 없습니다."
            )
        
        # DB에서 사용자 정보 조회
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
            detail=f"인증 처리 중 오류가 발생했습니다: {str(e)}"
        )

def get_user_id_from_token(token: str) -> str:
    """토큰에서 사용자 ID만 추출 (서비스 레이어에서 사용)"""
    try:
        payload = jwt_util.verify_token(token)
        user_id = payload.get("uid")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="토큰에 사용자 정보가 없습니다."
            )
        
        return user_id
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"토큰 검증 중 오류가 발생했습니다: {str(e)}"
        ) 