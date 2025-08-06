from fastapi import APIRouter, Depends
from typing import Dict, Any
from login.oauth_jwt_auth import get_current_user
from domain.User import User
from globals import create_success_response, ErrorCode, raise_business_exception

router = APIRouter(prefix="/auth")

@router.get("/me", summary="현재 사용자 정보 조회")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """현재 로그인된 사용자의 정보를 반환합니다."""
    try:
        user_info = {
            "uid": current_user.uid,
            "name": current_user.name,
            "email": current_user.email,
            "gradeNum": current_user.gradeNum,
            "termNum": current_user.termNum
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

@router.get("/verify", summary="토큰 유효성 검증")
async def verify_token(current_user: User = Depends(get_current_user)):
    """현재 토큰의 유효성을 검증합니다."""
    try:
        return create_success_response(
            {"valid": True, "user_id": current_user.uid},
            "토큰이 유효합니다."
        )
    except Exception as e:
        raise_business_exception(
            ErrorCode.UNAUTHORIZED,
            f"토큰 검증 실패: {str(e)}"
        ) 