from fastapi import HTTPException
from enum import Enum
from typing import Optional, Dict, Any

class ErrorCode(Enum):
    """에러 코드 정의"""
    # 공통 에러 (1000-1999)
    UNKNOWN_ERROR = (1000, "알 수 없는 오류가 발생했습니다.")
    INVALID_REQUEST = (1001, "잘못된 요청입니다.")
    UNAUTHORIZED = (1002, "인증이 필요합니다.")
    FORBIDDEN = (1003, "접근 권한이 없습니다.")
    NOT_FOUND = (1004, "요청한 리소스를 찾을 수 없습니다.")
    VALIDATION_ERROR = (1005, "입력 데이터가 올바르지 않습니다.")
    
    # 사용자 관련 에러 (2000-2999)
    USER_NOT_FOUND = (2000, "사용자를 찾을 수 없습니다.")
    USER_ALREADY_EXISTS = (2001, "이미 존재하는 사용자입니다.")
    USER_EMAIL_EXISTS = (2002, "이미 사용 중인 이메일입니다.")
    USER_INVALID_CREDENTIALS = (2003, "잘못된 인증 정보입니다.")
    
    # 파일 관련 에러 (3000-3999)
    FILE_NOT_FOUND = (3000, "파일을 찾을 수 없습니다.")
    FILE_UPLOAD_ERROR = (3001, "파일 업로드 중 오류가 발생했습니다.")
    FILE_TYPE_NOT_SUPPORTED = (3002, "지원하지 않는 파일 형식입니다.")
    FILE_SIZE_TOO_LARGE = (3003, "파일 크기가 너무 큽니다.")
    
    # 검사 관련 에러 (4000-4999)
    HMT_NOT_FOUND = (4000, "흥미검사를 찾을 수 없습니다.")
    HMT_PROCESSING_ERROR = (4001, "흥미검사 처리 중 오류가 발생했습니다.")
    CST_NOT_FOUND = (4100, "직업적성검사를 찾을 수 없습니다.")
    CST_PROCESSING_ERROR = (4101, "직업적성검사 처리 중 오류가 발생했습니다.")
    
    # 데이터베이스 관련 에러 (5000-5999)
    DATABASE_ERROR = (5000, "데이터베이스 오류가 발생했습니다.")
    TRANSACTION_ERROR = (5001, "트랜잭션 처리 중 오류가 발생했습니다.")
    
    # 외부 서비스 관련 에러 (6000-6999)
    S3_UPLOAD_ERROR = (6000, "파일 업로드 서비스 오류가 발생했습니다.")
    PDF_PROCESSING_ERROR = (6001, "PDF 처리 중 오류가 발생했습니다.")
    AI_PROCESSING_ERROR = (6002, "AI 분석 처리 중 오류가 발생했습니다.")

class CustomException(Exception):
    """커스텀 예외 클래스"""
    def __init__(self, error_code: ErrorCode, detail: Optional[str] = None, **kwargs):
        self.error_code = error_code
        self.detail = detail or error_code.value[1]
        self.kwargs = kwargs
        super().__init__(self.detail)

    def to_dict(self) -> Dict[str, Any]:
        """예외를 딕셔너리로 변환"""
        return {
            "error_code": self.error_code.value[0],
            "error_message": self.detail,
            "error_type": self.error_code.name,
            **self.kwargs
        }

class BusinessException(CustomException):
    """비즈니스 로직 예외"""
    pass

class ValidationException(CustomException):
    """검증 예외"""
    pass

class DatabaseException(CustomException):
    """데이터베이스 예외"""
    pass

class FileException(CustomException):
    """파일 처리 예외"""
    pass

def create_http_exception(exception: CustomException) -> HTTPException:
    """커스텀 예외를 HTTPException으로 변환"""
    error_code = exception.error_code.value[0]
    
    # HTTP 상태 코드 매핑
    status_code_mapping = {
        # 4xx 클라이언트 에러
        1001: 400,  # INVALID_REQUEST
        1002: 401,  # UNAUTHORIZED
        1003: 403,  # FORBIDDEN
        1004: 404,  # NOT_FOUND
        1005: 422,  # VALIDATION_ERROR
        2000: 404,  # USER_NOT_FOUND
        2001: 409,  # USER_ALREADY_EXISTS
        2002: 409,  # USER_EMAIL_EXISTS
        2003: 401,  # USER_INVALID_CREDENTIALS
        3000: 404,  # FILE_NOT_FOUND
        3001: 400,  # FILE_UPLOAD_ERROR
        3002: 400,  # FILE_TYPE_NOT_SUPPORTED
        3003: 413,  # FILE_SIZE_TOO_LARGE
        4000: 404,  # HMT_NOT_FOUND
        4001: 500,  # HMT_PROCESSING_ERROR
        4100: 404,  # CST_NOT_FOUND
        4101: 500,  # CST_PROCESSING_ERROR
    }
    
    status_code = status_code_mapping.get(error_code, 500)
    
    return HTTPException(
        status_code=status_code,
        detail=exception.to_dict()
    )

# 편의 함수들
def raise_business_exception(error_code: ErrorCode, detail: Optional[str] = None, **kwargs):
    """비즈니스 예외 발생"""
    raise BusinessException(error_code, detail, **kwargs)

def raise_validation_exception(error_code: ErrorCode, detail: Optional[str] = None, **kwargs):
    """검증 예외 발생"""
    raise ValidationException(error_code, detail, **kwargs)

def raise_database_exception(error_code: ErrorCode, detail: Optional[str] = None, **kwargs):
    """데이터베이스 예외 발생"""
    raise DatabaseException(error_code, detail, **kwargs)

def raise_file_exception(error_code: ErrorCode, detail: Optional[str] = None, **kwargs):
    """파일 예외 발생"""
    raise FileException(error_code, detail, **kwargs) 