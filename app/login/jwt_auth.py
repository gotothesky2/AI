import jwt
import os
import logging
from datetime import datetime, timezone
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from repository.userRepository import userRepository
from repository.oauthRepository import oauthRepository
from domain.User import User

# 로깅 설정
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

security = HTTPBearer()

class JwtAuthService:
    def __init__(self):
        # JWT_SECRET_KEY 환경 변수 사용
        self.secret_key = os.getenv("JWT_SECRET_KEY", "JWT_SECRET_KEY")
        self.algorithm = "HS256"
        logger.info(f"JWT Auth Service 초기화 - Secret Key: {self.secret_key[:10]}...")

    def verify_token(self, token: str) -> dict:
        """JWT 토큰 검증 및 페이로드 추출"""
        try:
            logger.info(f"JWT 토큰 검증 시작: {token[:20]}...")
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            logger.info(f"JWT 토큰 검증 성공: {payload}")
            return payload
        except jwt.ExpiredSignatureError as e:
            logger.error(f"JWT 토큰 만료: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="토큰이 만료되었습니다."
            )
        except jwt.InvalidTokenError as e:
            logger.error(f"JWT 토큰 무효: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 토큰입니다."
            )
        except Exception as e:
            logger.error(f"JWT 토큰 검증 중 예외 발생: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"토큰 검증 실패: {str(e)}"
            )

    def get_provider_user_id_from_token(self, token: str) -> str:
        """토큰에서 provider_user_id 추출"""
        payload = self.verify_token(token)
        provider_user_id = payload.get("sub")  # JWT subject는 provider_user_id
        logger.info(f"토큰에서 추출한 provider_user_id: {provider_user_id}")
        if not provider_user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="토큰에 사용자 정보가 없습니다."
            )
        return str(provider_user_id)

    def get_authorities_from_token(self, token: str) -> list:
        """토큰에서 권한 정보 추출"""
        payload = self.verify_token(token)
        authorities = payload.get("authorities", "")
        if authorities:
            return authorities.split(",")
        return []

# 전역 인스턴스 생성
jwt_auth_service = JwtAuthService()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """JWT 토큰을 사용한 현재 사용자 인증 (provider_user_id로 OAuth 테이블 조회)"""
    token = credentials.credentials
    logger.info(f"현재 사용자 인증 시작: {token[:20]}...")

    # 1. JWT 토큰 검증 및 provider_user_id 추출
    provider_user_id = jwt_auth_service.get_provider_user_id_from_token(token)
    logger.info(f"추출된 provider_user_id: {provider_user_id}")

    # 2. OAuth 테이블에서 provider_user_id로 조회
    oauth_record = oauthRepository.findByProviderUserId(provider_user_id)
    if not oauth_record:
        logger.error(f"OAuth 정보를 찾을 수 없음: provider_user_id={provider_user_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="OAuth 정보를 찾을 수 없습니다."
        )

    # 3. 만료 확인 제거 (시간과 상관없이 인증)
    # OAuth 테이블의 만료 시간은 무시하고 JWT 토큰의 만료 시간만 확인

    # 4. OAuth 레코드의 uid로 사용자 정보 조회
    user = userRepository.getById(oauth_record.uid)
    if not user:
        logger.error(f"사용자를 찾을 수 없음: uid={oauth_record.uid}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다."
        )

    logger.info(f"사용자 인증 성공: {user.name} (uid={user.uid})")
    return user

def verify_token_only(token: str) -> dict:
    """토큰만 검증하고 페이로드 반환"""
    try:
        logger.info(f"토큰 검증 시작: {token[:20]}...")
        payload = jwt_auth_service.verify_token(token)
        result = {
            "valid": True,
            "provider_user_id": payload.get("sub"),
            "authorities": payload.get("authorities", "").split(",") if payload.get("authorities") else [],
            "exp": payload.get("exp"),
            "iat": payload.get("iat")
        }
        logger.info(f"토큰 검증 성공: {result}")
        return result
    except HTTPException as e:
        logger.error(f"토큰 검증 실패 (HTTPException): {e.detail}")
        return {"valid": False, "error": e.detail}
    except Exception as e:
        logger.error(f"토큰 검증 실패 (Exception): {e}")
        return {"valid": False, "error": str(e)} 