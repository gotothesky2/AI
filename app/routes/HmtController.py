from fastapi import APIRouter, UploadFile, File, Depends
from typing import List
from services.HmtService import hmtService
from DTO.HmtDTO import HmtResponse
from domain.Hmt import Hmt
from globals import (
    ErrorCode, 
    raise_business_exception, 
    raise_file_exception,
    BusinessException,
    FileException,
    DatabaseException
)
from globals import create_success_response

router = APIRouter(prefix="/hmt")

@router.post("", summary="흥미검사 생성")
async def create_hmt(
    file: UploadFile = File(..., description="PDF 파일"),
    user_id: str = "temp_user_id"  # TODO: JWT 인증 구현 후 실제 사용자 ID 사용
):
    """
    PDF 파일을 업로드하여 흥미검사를 생성합니다.
    """
    # 1. 기본 파일 검증 (라우트단 책임)
    if not file.filename.endswith('.pdf'):
        raise_file_exception(
            ErrorCode.FILE_TYPE_NOT_SUPPORTED, 
            f"API 요청 오류 - PDF 파일만 업로드 가능합니다. 업로드된 파일: {file.filename}"
        )
    
    try:
        # 2. 서비스단 호출
        result = hmtService.createHmt(user_id, file)
        return create_success_response(result, "흥미검사가 성공적으로 생성되었습니다.")
        
    except FileException as e:
        # 서비스단에서 올라온 파일 관련 예외를 라우트 컨텍스트로 재발생
        raise_file_exception(
            e.error_code,
            f"흥미검사 API 실패 - {e.detail}"
        )
    except BusinessException as e:
        # 서비스단에서 올라온 비즈니스 예외를 라우트 컨텍스트로 재발생
        raise_business_exception(
            e.error_code,
            f"흥미검사 API 실패 - {e.detail}"
        )
    except DatabaseException as e:
        # 서비스단에서 올라온 데이터베이스 예외를 라우트 컨텍스트로 재발생
        raise_business_exception(
            e.error_code,
            f"흥미검사 API 데이터베이스 오류 - {e.detail}"
        )
    except Exception as e:
        # 예상치 못한 예외
        raise_business_exception(
            ErrorCode.UNKNOWN_ERROR,
            f"흥미검사 API 예상치 못한 오류 - {str(e)}"
        )

@router.get("/{hmt_id}", summary="흥미검사 조회")
async def get_hmt(hmt_id: int):
    """
    특정 ID의 흥미검사를 조회합니다.
    """
    try:
        result = hmtService.getHmtById(hmt_id)
        return create_success_response(
            HmtResponse.model_validate(result, from_attributes=True),
            "흥미검사 조회가 완료되었습니다."
        )
    except BusinessException as e:
        # 서비스단 예외를 라우트 컨텍스트로 재발생
        raise_business_exception(
            e.error_code,
            f"흥미검사 조회 API 실패 - {e.detail}"
        )
    except Exception as e:
        raise_business_exception(
            ErrorCode.UNKNOWN_ERROR,
            f"흥미검사 조회 API 예상치 못한 오류 - {str(e)}"
        )

@router.get("/user/{user_id}", summary="사용자별 흥미검사 목록")
async def get_user_hmts(user_id: str):
    """
    특정 사용자의 모든 흥미검사를 조회합니다.
    """
    try:
        result = hmtService.allHmtByUserId(user_id)
        return create_success_response(result, "사용자별 흥미검사 목록 조회가 완료되었습니다.")
    except BusinessException as e:
        # 서비스단 예외를 라우트 컨텍스트로 재발생
        raise_business_exception(
            e.error_code,
            f"사용자별 흥미검사 목록 API 실패 - {e.detail}"
        )
    except Exception as e:
        raise_business_exception(
            ErrorCode.UNKNOWN_ERROR,
            f"사용자별 흥미검사 목록 API 예상치 못한 오류 - {str(e)}"
        )

@router.delete("/{hmt_id}", summary="흥미검사 삭제")
async def delete_hmt(hmt_id: int):
    """
    특정 ID의 흥미검사를 삭제합니다.
    """
    try:
        hmtService.deleteHmt(hmt_id)
        return create_success_response(message=f"흥미검사 ID {hmt_id}가 성공적으로 삭제되었습니다.")
    except BusinessException as e:
        # 서비스단 예외를 라우트 컨텍스트로 재발생
        raise_business_exception(
            e.error_code,
            f"흥미검사 삭제 API 실패 - {e.detail}"
        )
    except Exception as e:
        raise_business_exception(
            ErrorCode.UNKNOWN_ERROR,
            f"흥미검사 삭제 API 예상치 못한 오류 - {str(e)}"
        )