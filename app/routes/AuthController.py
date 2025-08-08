from fastapi import APIRouter, Depends
from typing import Dict, Any
from login.oauth_jwt_auth import get_current_user, verify_token
from login.jwt_auth import jwt_auth_service
from domain.User import User
from globals import create_success_response, ErrorCode, raise_business_exception

router = APIRouter(prefix="/auth")

@router.post("/test-token", summary="JWT 토큰 테스트")
async def test_jwt_token(token: str):
    """JWT 토큰을 테스트하고 상세 정보를 반환합니다."""
    try:
        # 토큰을 직접 디코딩해서 내용 확인
        import jwt
        import os
        
        # JWT_SECRET_KEY 환경 변수 사용
        secret_key = os.getenv("JWT_SECRET_KEY", "JWT_SECRET_KEY")
        
        # 서명 검증 없이 페이로드만 확인
        payload = jwt.decode(token, options={'verify_signature': False})
        
        # 서명 검증 시도
        try:
            verified_payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            signature_valid = True
        except Exception as e:
            signature_valid = False
            verification_error = str(e)
        
        return create_success_response(
            {
                "token_info": {
                    "payload": payload,
                    "signature_valid": signature_valid,
                    "secret_key": secret_key[:10] + "..." if len(secret_key) > 10 else secret_key,
                    "verification_error": verification_error if not signature_valid else None
                }
            },
            "JWT 토큰 테스트 완료"
        )
    except Exception as e:
        raise_business_exception(
            ErrorCode.UNKNOWN_ERROR,
            f"토큰 테스트 실패: {str(e)}"
        )

@router.get("/me", summary="현재 사용자 정보 조회")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """현재 로그인된 사용자의 정보를 반환합니다."""
    try:
        user_info = {
            "uid": current_user.uid,
            "name": current_user.name,
            "email": current_user.email,
            "gradeNum": current_user.gradeNum
        }
        return create_success_response(
            user_info,
            "현재 사용자 정보 조회가 완료되었습니다."
        )
    except Exception as e:
        raise_business_exception(
            ErrorCode.UNKNOWN_ERROR,
            f"사용자 정보 조회 중 오류: {str(e)}"
        )

@router.get("/verify", summary="JWT 토큰 유효성 검증")
async def verify_token_endpoint(current_user: User = Depends(get_current_user)):
    """현재 JWT 토큰의 유효성을 검증합니다."""
    try:
        return create_success_response(
            {"valid": True, "user_id": current_user.uid},
            "JWT 토큰이 유효합니다."
        )
    except Exception as e:
        raise_business_exception(
            ErrorCode.UNAUTHORIZED,
            f"JWT 토큰 검증 실패: {str(e)}"
        )

@router.post("/verify-token", summary="JWT 토큰 검증 (자바 백엔드용)")
async def verify_token_only_endpoint(token: str):
    """JWT 토큰만 검증하고 사용자 정보 반환 (자바 백엔드에서 호출)"""
    try:
        token_data = verify_token(token)
        if not token_data.get("valid"):
            return create_success_response(
                {"valid": False},
                "유효하지 않은 JWT 토큰입니다."
            )
        
        return create_success_response(
            {
                "valid": True,
                "provider_user_id": token_data.get("provider_user_id"),
                "authorities": token_data.get("authorities", []),
                "exp": token_data.get("exp"),
                "iat": token_data.get("iat")
            },
            "JWT 토큰이 유효합니다."
        )
    except Exception as e:
        raise_business_exception(
            ErrorCode.UNAUTHORIZED,
            f"JWT 토큰 검증 실패: {str(e)}"
        ) 

