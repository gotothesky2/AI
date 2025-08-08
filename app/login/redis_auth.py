import json
import os
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from redisClient import get_redis_client
from repository.userRepository import userRepository
from domain.User import User

security = HTTPBearer()

class RedisAuthService:
    def __init__(self):
        self.redis_client = get_redis_client()
        self.token_prefix = "auth_token:"

    def get_token_data(self, token: str) -> dict:
        """Redis에서 토큰 데이터 조회"""
        key = f"{self.token_prefix}{token}"
        data = self.redis_client.get(key)
        if data:
            return json.loads(data)
        return None

    def refresh_token(self, token: str):
        """토큰 만료 시간을 갱신 (자바 백엔드에서 설정한 만료 시간 유지)"""
        key = f"{self.token_prefix}{token}"
        data = self.redis_client.get(key)
        if data:
            # 기존 TTL을 유지하거나 약간 연장
            current_ttl = self.redis_client.ttl(key)
            if current_ttl > 0:
                # 5분 연장
                self.redis_client.expire(key, current_ttl + 300)

# 전역 인스턴스 생성
redis_auth_service = RedisAuthService()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Redis를 사용한 현재 사용자 인증 (자바 백엔드에서 생성된 토큰 검증)"""
    token = credentials.credentials

    # 1. Redis에서 토큰 데이터 조회
    token_data = redis_auth_service.get_token_data(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰입니다."
        )

    # 2. 사용자 정보 조회
    user_id = token_data.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰에 사용자 정보가 없습니다."
        )

    user = userRepository.getById(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다."
        )

    # 3. 토큰 갱신 (선택적)
    redis_auth_service.refresh_token(token)

    return user

def verify_token_only(token: str) -> dict:
    """토큰만 검증하고 사용자 정보 반환 (자바 백엔드용)"""
    token_data = redis_auth_service.get_token_data(token)
    if not token_data:
        return None
    return token_data 