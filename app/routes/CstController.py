from fastapi import APIRouter, UploadFile, File, Depends
from typing import List
from app.services.CstService import cstService
from app.DTO.CstDTO import CstResponse
from app.domain.Cst import Cst
from app.util.exceptions import (
    ErrorCode, 
    raise_business_exception, 
    raise_file_exception
)
from app.util.exception_handler import create_success_response

router = APIRouter(prefix="/cst")

@router.post("", summary="창의성검사 생성")
async def create_cst(
    file: UploadFile = File(..., description="PDF 파일"),
    user_id: str = "temp_user_id"  # TODO: JWT 인증 구현 후 실제 사용자 ID 사용
):
    """
    PDF 파일을 업로드하여 창의성검사를 생성합니다.
    """
    if not file.filename.endswith('.pdf'):
        raise_file_exception(ErrorCode.FILE_TYPE_NOT_SUPPORTED, "PDF 파일만 업로드 가능합니다.")
    
    try:
        result = cstService.createCst(user_id, file)
        return create_success_response(result, "창의성검사가 성공적으로 생성되었습니다.")
    except Exception as e:
        raise_business_exception(ErrorCode.CST_PROCESSING_ERROR, str(e))

@router.get("/{cst_id}", summary="창의성검사 조회")
async def get_cst(cst_id: int):
    """
    특정 ID의 창의성검사를 조회합니다.
    """
    try:
        result = cstService.getCstById(cst_id)
        return create_success_response(
            CstResponse.model_validate(result, from_attributes=True),
            "창의성검사 조회가 완료되었습니다."
        )
    except Exception as e:
        raise_business_exception(ErrorCode.CST_NOT_FOUND, str(e))

@router.get("/user/{user_id}", summary="사용자별 창의성검사 목록")
async def get_user_csts(user_id: str):
    """
    특정 사용자의 모든 창의성검사를 조회합니다.
    """
    try:
        result = cstService.allCstByUser(user_id)
        return create_success_response(result, "사용자별 창의성검사 목록 조회가 완료되었습니다.")
    except Exception as e:
        raise_business_exception(ErrorCode.CST_NOT_FOUND, str(e))

@router.delete("/{cst_id}", summary="창의성검사 삭제")
async def delete_cst(cst_id: int):
    """
    특정 ID의 창의성검사를 삭제합니다.
    """
    try:
        cstService.deleteCst(cst_id)
        return create_success_response(message=f"창의성검사 ID {cst_id}가 성공적으로 삭제되었습니다.")
    except Exception as e:
        raise_business_exception(ErrorCode.CST_NOT_FOUND, str(e)) 