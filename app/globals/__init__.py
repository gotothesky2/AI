"""
글로벌 패키지 (globals)
애플리케이션 전역에서 사용되는 에러 코드, 예외 처리, 응답 관리 등을 포함합니다.
"""

from .exceptions import (
    ErrorCode,
    CustomException,
    BusinessException,
    FileException,
    DatabaseException,
    ValidationException,
    create_http_exception,
    raise_business_exception,
    raise_file_exception,
    raise_database_exception,
    raise_validation_exception
)

from .exception_handler import (
    setup_exception_handlers,
    create_success_response,
    create_error_response,
    custom_exception_handler,
    validation_exception_handler,
    sqlalchemy_exception_handler,
    general_exception_handler
)

__all__ = [
    # 예외 클래스
    "ErrorCode",
    "CustomException", 
    "BusinessException",
    "FileException",
    "DatabaseException",
    "ValidationException",
    
    # 예외 생성/변환 함수
    "create_http_exception",
    "raise_business_exception",
    "raise_file_exception", 
    "raise_database_exception",
    "raise_validation_exception",
    
    # 예외 핸들러
    "setup_exception_handlers",
    "custom_exception_handler",
    "validation_exception_handler", 
    "sqlalchemy_exception_handler",
    "general_exception_handler",
    
    # 응답 생성 함수
    "create_success_response",
    "create_error_response"
] 