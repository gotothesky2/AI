from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.util.exceptions import (
    CustomException, 
    create_http_exception, 
    ErrorCode,
    raise_business_exception
)
import logging
import traceback
from typing import Union

logger = logging.getLogger(__name__)

async def custom_exception_handler(request: Request, exc: CustomException):
    """커스텀 예외 처리"""
    logger.error(f"Custom Exception: {exc.error_code.name} - {exc.detail}")
    
    return JSONResponse(
        status_code=create_http_exception(exc).status_code,
        content={
            "success": False,
            "error": exc.to_dict(),
            "path": str(request.url),
            "method": request.method
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """검증 예외 처리"""
    logger.error(f"Validation Error: {exc.errors()}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "error_code": ErrorCode.VALIDATION_ERROR.value[0],
                "error_message": "입력 데이터가 올바르지 않습니다.",
                "error_type": ErrorCode.VALIDATION_ERROR.name,
                "validation_errors": exc.errors()
            },
            "path": str(request.url),
            "method": request.method
        }
    )

async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """SQLAlchemy 예외 처리"""
    logger.error(f"Database Error: {str(exc)}")
    logger.error(traceback.format_exc())
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "error_code": ErrorCode.DATABASE_ERROR.value[0],
                "error_message": "데이터베이스 오류가 발생했습니다.",
                "error_type": ErrorCode.DATABASE_ERROR.name,
                "detail": str(exc) if logger.isEnabledFor(logging.DEBUG) else None
            },
            "path": str(request.url),
            "method": request.method
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    """일반 예외 처리"""
    logger.error(f"Unexpected Error: {str(exc)}")
    logger.error(traceback.format_exc())
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "error_code": ErrorCode.UNKNOWN_ERROR.value[0],
                "error_message": "알 수 없는 오류가 발생했습니다.",
                "error_type": ErrorCode.UNKNOWN_ERROR.name,
                "detail": str(exc) if logger.isEnabledFor(logging.DEBUG) else None
            },
            "path": str(request.url),
            "method": request.method
        }
    )

def setup_exception_handlers(app):
    """예외 핸들러 설정"""
    from fastapi import FastAPI
    
    # 커스텀 예외 핸들러 등록
    app.add_exception_handler(CustomException, custom_exception_handler)
    
    # FastAPI 기본 예외 핸들러 등록
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    
    # SQLAlchemy 예외 핸들러 등록
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    
    # 일반 예외 핸들러 등록 (마지막에 등록)
    app.add_exception_handler(Exception, general_exception_handler)

# 응답 래퍼 함수
def create_success_response(data: any = None, message: str = "성공"):
    """성공 응답 생성"""
    response = {
        "success": True,
        "message": message
    }
    if data is not None:
        response["data"] = data
    return response

def create_error_response(error_code: ErrorCode, detail: str = None, **kwargs):
    """에러 응답 생성"""
    return {
        "success": False,
        "error": {
            "error_code": error_code.value[0],
            "error_message": detail or error_code.value[1],
            "error_type": error_code.name,
            **kwargs
        }
    } 