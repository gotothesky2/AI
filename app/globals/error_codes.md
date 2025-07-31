# 에러 코드 문서

## 개요
이 문서는 AI 검사 시스템 API에서 사용되는 에러 코드들을 설명합니다.

## 에러 코드 체계

### 공통 에러 (1000-1999)
| 코드 | 에러명 | 설명 | HTTP 상태 코드 |
|------|--------|------|----------------|
| 1000 | UNKNOWN_ERROR | 알 수 없는 오류가 발생했습니다. | 500 |
| 1001 | INVALID_REQUEST | 잘못된 요청입니다. | 400 |
| 1002 | UNAUTHORIZED | 인증이 필요합니다. | 401 |
| 1003 | FORBIDDEN | 접근 권한이 없습니다. | 403 |
| 1004 | NOT_FOUND | 요청한 리소스를 찾을 수 없습니다. | 404 |
| 1005 | VALIDATION_ERROR | 입력 데이터가 올바르지 않습니다. | 422 |

### 사용자 관련 에러 (2000-2999)
| 코드 | 에러명 | 설명 | HTTP 상태 코드 |
|------|--------|------|----------------|
| 2000 | USER_NOT_FOUND | 사용자를 찾을 수 없습니다. | 404 |
| 2001 | USER_ALREADY_EXISTS | 이미 존재하는 사용자입니다. | 409 |
| 2002 | USER_EMAIL_EXISTS | 이미 사용 중인 이메일입니다. | 409 |
| 2003 | USER_INVALID_CREDENTIALS | 잘못된 인증 정보입니다. | 401 |

### 파일 관련 에러 (3000-3999)
| 코드 | 에러명 | 설명 | HTTP 상태 코드 |
|------|--------|------|----------------|
| 3000 | FILE_NOT_FOUND | 파일을 찾을 수 없습니다. | 404 |
| 3001 | FILE_UPLOAD_ERROR | 파일 업로드 중 오류가 발생했습니다. | 400 |
| 3002 | FILE_TYPE_NOT_SUPPORTED | 지원하지 않는 파일 형식입니다. | 400 |
| 3003 | FILE_SIZE_TOO_LARGE | 파일 크기가 너무 큽니다. | 413 |

### 검사 관련 에러 (4000-4999)
| 코드 | 에러명 | 설명 | HTTP 상태 코드 |
|------|--------|------|----------------|
| 4000 | HMT_NOT_FOUND | 흥미검사를 찾을 수 없습니다. | 404 |
| 4001 | HMT_PROCESSING_ERROR | 흥미검사 처리 중 오류가 발생했습니다. | 500 |
| 4100 | CST_NOT_FOUND | 창의성검사를 찾을 수 없습니다. | 404 |
| 4101 | CST_PROCESSING_ERROR | 창의성검사 처리 중 오류가 발생했습니다. | 500 |

### 데이터베이스 관련 에러 (5000-5999)
| 코드 | 에러명 | 설명 | HTTP 상태 코드 |
|------|--------|------|----------------|
| 5000 | DATABASE_ERROR | 데이터베이스 오류가 발생했습니다. | 500 |
| 5001 | TRANSACTION_ERROR | 트랜잭션 처리 중 오류가 발생했습니다. | 500 |

### 외부 서비스 관련 에러 (6000-6999)
| 코드 | 에러명 | 설명 | HTTP 상태 코드 |
|------|--------|------|----------------|
| 6000 | S3_UPLOAD_ERROR | 파일 업로드 서비스 오류가 발생했습니다. | 500 |
| 6001 | PDF_PROCESSING_ERROR | PDF 처리 중 오류가 발생했습니다. | 500 |
| 6002 | AI_PROCESSING_ERROR | AI 분석 처리 중 오류가 발생했습니다. | 500 |

## 응답 형식

### 성공 응답
```json
{
  "success": true,
  "message": "성공 메시지",
  "data": {
    // 응답 데이터
  }
}
```

### 에러 응답
```json
{
  "success": false,
  "error": {
    "error_code": 2000,
    "error_message": "사용자를 찾을 수 없습니다.",
    "error_type": "USER_NOT_FOUND",
    "detail": "추가 상세 정보 (선택사항)"
  },
  "path": "/api/users/123",
  "method": "GET"
}
```

## 사용 예시

### Python에서 에러 발생
```python
from app.util.exceptions import raise_business_exception, ErrorCode

# 사용자를 찾을 수 없는 경우
raise_business_exception(ErrorCode.USER_NOT_FOUND, "사용자 ID 123을 찾을 수 없습니다.")

# 파일 형식이 지원되지 않는 경우
raise_file_exception(ErrorCode.FILE_TYPE_NOT_SUPPORTED, "PDF 파일만 업로드 가능합니다.")
```

### JavaScript에서 에러 처리
```javascript
fetch('/api/users/123')
  .then(response => response.json())
  .then(data => {
    if (!data.success) {
      console.error(`에러 코드: ${data.error.error_code}`);
      console.error(`에러 메시지: ${data.error.error_message}`);
      console.error(`에러 타입: ${data.error.error_type}`);
    }
  });
```

## 에러 코드 추가 방법

1. `app/util/exceptions.py`의 `ErrorCode` enum에 새로운 에러 코드 추가
2. `create_http_exception` 함수의 `status_code_mapping`에 HTTP 상태 코드 매핑 추가
3. 이 문서에 새로운 에러 코드 정보 추가 