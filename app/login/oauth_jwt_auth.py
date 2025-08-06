from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from login.jwt_util import jwt_util
from domain.User import User
from domain.OAuth import OAuth
from repository.userRepository import userRepository
from repository.oauthRepository import oauthRepository

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
        
        # OAuth 테이블에서 액세스 토큰 확인
        oauth_record = oauthRepository.findByAccessToken(token)
        if not oauth_record:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 액세스 토큰입니다."
            )
        
        # 토큰 만료 확인
        if oauth_record.expireDate < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="액세스 토큰이 만료되었습니다."
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

def create_oauth_record(user_id: str, access_token: str, provider: str = "JWT", expire_hours: int = 24) -> OAuth:
    """OAuth 테이블에 액세스 토큰 기록 생성"""
    expire_date = datetime.now() + timedelta(hours=expire_hours)
    
    oauth_record = OAuth(
        providerUserId=user_id,
        accessToken=access_token,
        expireDate=expire_date,
        provider=provider,
        uid=user_id
    )
    
    oauthRepository.save(oauth_record)
    return oauth_record

def invalidate_oauth_token(access_token: str) -> bool:
    """OAuth 테이블에서 액세스 토큰 삭제 (로그아웃)"""
    try:
        oauth_record = oauthRepository.findByAccessToken(access_token)
        if oauth_record:
            oauthRepository.remove(oauth_record)
            return True
        return False
    except Exception:
        return False 