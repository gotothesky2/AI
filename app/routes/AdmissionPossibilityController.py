from fastapi import APIRouter, Depends
from typing import Dict
from services.AdmissionPossibilityService import admissionPossibilityService
from login.oauth_jwt_auth import get_current_user
from domain.User import User
from globals import create_success_response, ErrorCode, raise_business_exception

router = APIRouter(prefix="/api/admission-possibility", tags=["합격가능성"])

@router.get("/my", summary="내 합격가능성 조회")
async def get_my_admission_possibility(
    current_user: User = Depends(get_current_user)
) -> Dict:
    """
    현재 로그인된 사용자의 북마크된 학과-학교에 대한 합격가능성을 분석합니다.
    
    Returns:
        Dict: 합격가능성 분석 결과
    """
    try:
        result = admissionPossibilityService.getUserAdmissionPossibility(current_user.uid)
        
        if "error" in result:
            raise_business_exception(
                ErrorCode.UNKNOWN_ERROR,
                result["error"]
            )
        
        return create_success_response(
            result,
            "합격가능성 분석이 완료되었습니다."
        )
        
    except Exception as e:
        raise_business_exception(
            ErrorCode.UNKNOWN_ERROR,
            f"합격가능성 분석 중 오류가 발생했습니다: {str(e)}"
        )

@router.get("/bookmark/{bookmark_id}", summary="특정 북마크 합격가능성 조회")
async def get_bookmark_possibility(
    bookmark_id: int,
    current_user: User = Depends(get_current_user)
) -> Dict:
    """
    특정 북마크에 대한 합격가능성을 분석합니다.
    
    Args:
        bookmark_id: 북마크 ID
        
    Returns:
        Dict: 특정 북마크의 합격가능성 분석 결과
    """
    try:
        result = admissionPossibilityService.getSpecificBookmarkPossibility(current_user.uid, bookmark_id)
        
        if "error" in result:
            raise_business_exception(
                ErrorCode.UNKNOWN_ERROR,
                result["error"]
            )
        
        return create_success_response(
            result,
            "북마크 합격가능성 분석이 완료되었습니다."
        )
        
    except Exception as e:
        raise_business_exception(
            ErrorCode.UNKNOWN_ERROR,
            f"북마크 분석 중 오류가 발생했습니다: {str(e)}"
        )

@router.get("/summary", summary="내 합격가능성 요약 조회")
async def get_admission_possibility_summary(
    current_user: User = Depends(get_current_user)
) -> Dict:
    """
    현재 로그인된 사용자의 합격가능성 요약 정보를 제공합니다.
    
    Returns:
        Dict: 합격가능성 요약 정보
    """
    try:
        result = admissionPossibilityService.getUserAdmissionPossibility(current_user.uid)
        
        if "error" in result:
            raise_business_exception(
                ErrorCode.UNKNOWN_ERROR,
                result["error"]
            )
        
        # 요약 정보만 추출
        if "analysis" in result and result["analysis"]:
            summary = result["analysis"].get("summary", {})
            return create_success_response(
                {
                    "uid": current_user.uid,
                    "summary": summary
                },
                "합격가능성 요약 조회가 완료되었습니다."
            )
        else:
            return create_success_response(
                {
                    "uid": current_user.uid,
                    "summary": {"message": "분석할 북마크가 없습니다."}
                },
                "북마크가 없습니다."
            )
        
    except Exception as e:
        raise_business_exception(
            ErrorCode.UNKNOWN_ERROR,
            f"합격가능성 요약 조회 중 오류가 발생했습니다: {str(e)}"
        )
