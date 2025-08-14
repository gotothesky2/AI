import jwt
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from dotenv import load_dotenv
import pytz

load_dotenv()


class JWTUtil:
    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET_KEY")
        self.algorithm = "HS256"

        # 환경변수에서 만료 시간 설정 가져오기 (초 단위)
        self.token_expiration = int(os.getenv("JWT_EXPIRATION", "3600"))  # 1시간 (3600초)
        self.refresh_token_expiration = int(os.getenv("JWT_REFRESH_EXPIRATION", "86400"))  # 1일 (86400초)

        if not self.secret_key:
            raise ValueError("JWT_SECRET_KEY 환경변수가 설정되지 않았습니다.")

    def verify_token(self, token: str) -> Dict[str, Any]:
        """JWT 토큰 검증 및 페이로드 반환"""
        try:
            # 서울 시간대 설정
            seoul_tz = pytz.timezone('Asia/Seoul')
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # 토큰 만료 시간을 서울 시간대로 변환하여 로깅
            if 'exp' in payload:
                exp_timestamp = payload['exp']
                exp_datetime = datetime.fromtimestamp(exp_timestamp, seoul_tz)
                print(f"토큰 만료 시간 (서울): {exp_datetime}")
            
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="토큰이 만료되었습니다."
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 토큰입니다."
            )

    def get_user_id_from_token(self, token: str) -> str:
        """토큰에서 사용자 ID 추출"""
        payload = self.verify_token(token)
        user_id = payload.get("uid")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="토큰에 사용자 정보가 없습니다."
            )

        return user_id

    def create_token(self, user_id: str, expires_delta: timedelta = None) -> str:
        """JWT 토큰 생성 (환경변수 사용)"""
        # 서울 시간대 설정
        seoul_tz = pytz.timezone('Asia/Seoul')
        
        if expires_delta:
            expire = datetime.now(seoul_tz) + expires_delta
        else:
            # 기본값으로 환경변수 사용
            expire = datetime.now(seoul_tz) + timedelta(seconds=self.token_expiration)

        to_encode = {"uid": user_id, "exp": expire}
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt


# 싱글톤 인스턴스
jwt_util = JWTUtil() 