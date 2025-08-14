# AI 검사 시스템 API


### 🔍 주요 검사 유형

#### 📊 흥미검사 (HMT - Holland's Theory)
- **RIASEC 모델** 기반 6개 흥미 영역 분석
- **R**: 현실형 (Realistic) - 실용적, 기계적
- **I**: 탐구형 (Investigative) - 분석적, 지적
- **A**: 예술형 (Artistic) - 창의적, 표현적
- **S**: 사회형 (Social) - 협력적, 교육적
- **E**: 진취형 (Enterprising) - 설득적, 관리적
- **C**: 관습형 (Conventional) - 체계적, 사무적

#### 🎯 직업적성검사 (CST - Career Skills Test)
- **11개 능력영역** 종합 분석
- 수리·논리력, 예술시각능력, 손재능, 공간지각력, 음악능력
- 대인관계능력, 창의력, 언어능력, 신체·운동능력, 자연친화력, 자기성찰능력

## 🏗️ 아키텍처

### 📁 프로젝트 구조
```
AI/
├── app/                          # 메인 애플리케이션
│   ├── run.py                   # FastAPI 서버 실행 파일
│   ├── db.py                    # 데이터베이스 설정
│   ├── domain/                  # 도메인 모델
│   │   ├── entity/
│   │   │   └── BaseEntity.py    # 기본 엔티티 (생성/수정 시간 자동 관리)
│   │   ├── User.py              # 사용자 엔티티
│   │   ├── Hmt.py               # 흥미검사 엔티티
│   │   ├── Cst.py               # 직업적성검사 엔티티
│   │   ├── AiReport.py          # AI 분석 리포트 엔티티
│   │   ├── Report.py            # 리포트 엔티티
│   │   ├── ReportScore.py       # 리포트 점수 엔티티
│   │   ├── Mock.py              # 모의고사 엔티티
│   │   ├── MockScore.py         # 모의고사 점수 엔티티
│   │   ├── Major.py             # 전공 엔티티
│   │   ├── Field.py             # 분야 엔티티
│   │   ├── University.py        # 대학교 엔티티
│   │   ├── UniversityMajor.py   # 대학-전공 연관 엔티티
│   │   └── OAuth.py             # OAuth 인증 엔티티
│   ├── DTO/                     # 데이터 전송 객체
│   │   ├── HmtDTO.py            # 흥미검사 DTO
│   │   ├── CstDTO.py            # 직업적성검사 DTO
│   │   ├── UserDTO.py           # 사용자 DTO
│   │   └── AiRepotDto.py        # AI 리포트 DTO
│   ├── repository/               # 데이터 접근 계층
│   │   ├── Repository.py        # 기본 레포지토리 (CRUD 공통 로직)
│   │   ├── userRepository.py    # 사용자 레포지토리
│   │   ├── hmtRepository.py     # 흥미검사 레포지토리
│   │   ├── cstRepository.py     # 직업적성검사 레포지토리
│   │   ├── aiReportRepository.py # AI 리포트 레포지토리
│   │   ├── reportRepository.py  # 리포트 레포지토리
│   │   ├── mockRepository.py    # 모의고사 레포지토리
│   │   ├── majorRepository.py   # 전공 레포지토리
│   │   ├── fieldRepository.py   # 분야 레포지토리
│   │   ├── universityRepository.py # 대학교 레포지토리
│   │   └── oauthRepository.py   # OAuth 레포지토리
│   ├── services/                 # 비즈니스 로직
│   │   ├── HmtService.py        # 흥미검사 서비스
│   │   ├── CstService.py        # 직업적성검사 서비스
│   │   ├── UserService.py       # 사용자 서비스
│   │   ├── AiReportService.py   # AI 리포트 서비스
│   │   └── ReportService.py     # 리포트 서비스
│   ├── routes/                   # API 라우터
│   │   ├── HmtController.py     # 흥미검사 컨트롤러
│   │   ├── CstController.py     # 직업적성검사 컨트롤러
│   │   └── AuthController.py    # 인증 컨트롤러
│   ├── login/                    # 인증 시스템
│   │   ├── jwt_auth.py          # JWT 인증 서비스
│   │   ├── jwt_util.py          # JWT 유틸리티
│   │   ├── oauth_jwt_auth.py    # OAuth + JWT 통합 인증
│   │   ├── redis_auth.py        # Redis 인증
│   │   └── jwtUser.py           # JWT 사용자 모델
│   ├── gptApi/                   # GPT API 연동
│   │   ├── gptEngine.py         # GPT 엔진 (추상 클래스)
│   │   ├── testReportEng/       # 테스트 리포트 엔진
│   │   │   └── testReport.py    # 테스트 리포트 생성
│   │   └── test.py              # GPT API 테스트
│   ├── util/                     # 유틸리티
│   │   ├── Transactional.py     # 트랜잭션 데코레이터 (읽기/쓰기 분리)
│   │   ├── globalDB/            # 글로벌 DB 컨텍스트
│   │   │   ├── db_context.py    # DB 컨텍스트 관리
│   │   │   └── global_db.py     # 글로벌 DB 접근
│   │   ├── PdfExtracter/        # PDF 처리 엔진
│   │   │   ├── HmtExtracter.py  # 흥미검사 PDF 분석
│   │   │   └── CstExtracter.py  # 직업적성검사 PDF 분석
│   │   ├── S3/                  # AWS S3 연동
│   │   │   └── S3_Util.py       # S3 파일 업로드/다운로드
│   │   ├── auth_dependency.py   # 인증 의존성
│   │   └── termGenerator.py     # 학기 생성기
│   ├── globals/                  # 전역 설정
│   │   ├── exceptions.py        # 커스텀 예외 및 에러코드
│   │   ├── exception_handler.py # 전역 예외 처리기
│   │   └── error_codes.md       # 에러코드 문서
│   ├── redisClient.py           # Redis 클라이언트
│   └── __init__.py
├── PdfExtractor/                 # PDF 추출 테스트
├── Test/                         # 테스트 코드
├── pytest.ini                   # pytest 설정
├── requirements.txt              # Python 의존성
└── README.md                     # 프로젝트 문서
```

## 🛠️ 기술 스택

### 🔧 Backend
- **Framework**: FastAPI 0.116.1
- **Language**: Python 3.8+
- **ORM**: SQLAlchemy 2.0.41
- **Database**: MySQL (PyMySQL 1.1.1)
- **Authentication**: JWT + OAuth
- **Cache**: Redis 6.2.0

### 🚀 AI & ML
- **AI Engine**: OpenAI GPT-4o
- **PDF Processing**: PyMuPDF (fitz) 1.26.3
- **Data Analysis**: Custom scoring algorithms

### ☁️ Cloud & Storage
- **Storage**: AWS S3 (boto3 1.34.44)
- **File Handling**: FastAPI UploadFile
- **Environment**: python-dotenv 1.1.1

### 🔒 Security & Performance
- **CORS**: FastAPI CORS Middleware
- **Validation**: Pydantic 2.11.7
- **Async Support**: uvicorn 0.27.1 + uvloop 0.21.0
- **Testing**: pytest 8.4.1

## 🚀 시작하기

### 1. 환경 설정

```bash
# 프로젝트 클론
git clone <repository-url>
cd AI

# Python 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# 의존성 설치
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일을 생성하고 다음 변수들을 설정하세요:

```env
GPT_API_KEY=

DB_SELECT=LOCAL

#LOCAL
LOCAL_HOST=
LOCAL_USER=
LOCAL_PASSWORD=
LOCAL_PORT=
LOCAL_NAME=

#AWS
AWS_USER=
AWS_PASSWORD=
AWS_ADDRESS=
AWS_NAME=
AWS_PORT=

#S3
AWS_S3_BUCKET_NAME=
AWS_S3_ACCESS_KEY=
AWS_S3_SECRET_KEY=

#JWT
JWT_SECRET_KEY=
JWT_EXPIRATION=3600
JWT_REFRESH_EXPIRATION=86400

#Radis
REDIS_HOST=
REDIS_PORT=
```

### 3. 데이터베이스 설정

MySQL 데이터베이스가 실행 중이어야 하며, `app/db.py`에서 연결 정보를 확인하세요.

### 4. 서버 실행

```bash
# app 폴더로 이동
cd app

# 서버 실행
python run.py
```

서버가 시작되면 다음 주소에서 접근 가능합니다:
- **API 서버**: http://localhost:8081
- **Swagger UI**: http://localhost:8081/docs
- **ReDoc**: http://localhost:8081/redoc

## 📖 API 문서

### 🔐 인증

모든 API는 JWT 토큰 인증이 필요합니다. `Authorization: Bearer <token>` 헤더를 포함해야 합니다.

### 📊 흥미검사 API

#### POST /hmt
흥미검사 PDF 파일을 업로드하여 분석합니다.

**요청**:
- `file`: PDF 파일 (multipart/form-data)
- `Authorization`: Bearer JWT 토큰

**응답**:
```json
{
  "success": true,
  "message": "흥미검사가 성공적으로 생성되었습니다.",
  "data": {
    "id": 16,
    "rScore": 48.9,
    "iScore": 62.1,
    "aScore": 48.8,
    "sScore": 19.1,
    "eScore": 54.9,
    "cScore": 25.1,
    "uploadTime": "2025-08-14T11:28:53.921226",
    "hmtTermNum": 2,
    "hmtGradeNum": 2,
    "DownloadUrl": null
  }
}
```

#### GET /hmt/my
현재 사용자의 모든 흥미검사를 조회합니다.

#### GET /hmt/{hmt_id}
특정 ID의 흥미검사를 조회합니다.

#### DELETE /hmt/{hmt_id}
흥미검사를 삭제합니다.

### 🎯 직업적성검사 API

#### POST /cst
직업적성검사 PDF 파일을 업로드하여 분석합니다.

**요청**:
- `file`: PDF 파일 (multipart/form-data)
- `Authorization`: Bearer JWT 토큰

**응답**:
```json
{
  "success": true,
  "message": "직업적성검사가 성공적으로 생성되었습니다.",
  "data": {
    "id": 3,
    "cstGradeNum": 2,
    "cstTermNum": 2,
    "uploadTime": "2025-08-14T11:30:16.569160",
    "mathScore": 98.5,
    "spaceScore": 95.9,
    "creativeScore": 91.1,
    "natureScore": 79.8,
    "artScore": 62.6,
    "musicScore": 61.6,
    "langScore": 47.3,
    "selfScore": 31.5,
    "handScore": 27.8,
    "relationScore": 7.6,
    "physicalScore": 0.3,
    "downloadUrl": null
  }
}
```

#### GET /cst/my
현재 사용자의 모든 직업적성검사를 조회합니다.

#### GET /cst/{cst_id}
특정 ID의 직업적성검사를 조회합니다.

#### DELETE /cst/{cst_id}
직업적성검사를 삭제합니다.

### 🧪 테스트 API

#### GET /test-error
예외 처리 테스트용 엔드포인트

#### GET /health
서버 상태 확인

## 🔧 핵심 기능

### 📄 PDF 처리 엔진

#### HmtExtracter
- **파일 검증**: PDF 형식, 페이지 수, 내용 키워드 확인
- **점수 추출**: RIASEC 6개 영역별 점수 자동 추출
- **에러 처리**: 직업적성검사 PDF와 구분하여 적절한 에러 메시지 제공

#### CstExtracter
- **파일 검증**: 직업적성검사 전용 PDF 확인
- **점수 추출**: 11개 능력영역별 점수 자동 추출
- **데이터 검증**: 모든 점수가 추출되었는지 확인

### 🤖 GPT AI 엔진

#### GptBase (추상 클래스)
- **모델**: GPT-4o
- **응답 형식**: JSON 강제
- **토큰 제한**: 3000
- **온도**: 0.6 (창의성과 일관성의 균형)

#### 구현체
- **TestReportEngine**: 테스트 결과 기반 맞춤형 리포트 생성

### 🔐 인증 시스템

#### JWT + OAuth 통합
- **토큰 검증**: 자동 만료 확인
- **사용자 조회**: OAuth 테이블 → User 테이블 연쇄 조회
- **권한 관리**: authorities 기반 접근 제어

#### Redis 연동
- **세션 관리**: 사용자 세션 정보 캐싱
- **토큰 저장**: 리프레시 토큰 관리

### 💾 데이터베이스 설계

#### BaseEntity
- **자동 타임스탬프**: `created_at`, `updated_at`
- **테이블명 자동화**: 클래스명 기반 snake_case 변환

#### 관계 설정
- **User ↔ Hmt**: 1:N (사용자당 여러 흥미검사)
- **User ↔ Cst**: 1:N (사용자당 여러 직업적성검사)
- **User ↔ AiReport**: 1:N (사용자당 여러 AI 리포트)

### 🔄 트랜잭션 관리

#### Transactional 데코레이터
- **@Transactional**: 기본 트랜잭션 (자동 커밋)
- **@TransactionalRead**: 읽기 전용 (커밋 없음)
- **@TransactionalWrite**: 쓰기 전용 (명시적 커밋)

#### 성능 최적화
- **배치 처리**: `save_all()` 메서드로 대량 데이터 처리
- **연결 풀**: 최적화된 DB 연결 관리

## 🚨 에러 처리
*: OAuth 테이블 → User 테이블 연쇄 조회
- **권한 관리**: authorities 기반 접근 제어

#### Redis 연동
- **세션 관리**: 사용자 세션 정보 캐싱
- **토큰 저장**: 리프레시 토큰 관리

### 💾 데이터베이스 설계

#### BaseEntity
- **자동 타임스탬프**: `created_at`, `updated_at`
- **테이블명 자동화**: 클래스명 기반 snake_case 변환

#### 관계 설정
- **User ↔ Hmt**: 1:N (사용자당 여러 흥미검사)
- **User ↔ Cst**: 1:N (사용자당 여러 직업적성검사)
- **User ↔ AiReport**: 1:N (사용자당 여러 AI 리포트)

### 🔄 트랜잭션 관리

#### Transactional 데코레이터
- **@Transactional**: 기본 트랜잭션 (자동 커밋)
- **@TransactionalRead**: 읽기 전용 (커밋 없음)
- **@TransactionalWrite**: 쓰기 전용 (명시적 커밋)

#### 성능 최적화
- **배치 처리**: `save_all()` 메서드로 대량 데이터 처리
- **연결 풀**: 최적화된 DB 연결 관리

## 🚨 에러 처리

### 체계적 에러코드 시스템

```python
class ErrorCode(Enum):
    # 공통 에러 (1000-1999)
    UNKNOWN_ERROR = (1000, "알 수 없는 오류가 발생했습니다.")
    VALIDATION_ERROR = (1005, "입력 데이터가 올바르지 않습니다.")
    
    # 사용자 관련 에러 (2000-2999)
    USER_NOT_FOUND = (2000, "사용자를 찾을 수 없습니다.")
    
    # 파일 관련 에러 (3000-3999)
    FILE_TYPE_NOT_SUPPORTED = (3002, "지원하지 않는 파일 형식입니다.")
    
    # 검사 관련 에러 (4000-4999)
    HMT_PROCESSING_ERROR = (4001, "흥미검사 처리 중 오류가 발생했습니다.")
    CST_PROCESSING_ERROR = (4101, "직업적성검사 처리 중 오류가 발생했습니다.")
    
    # 외부 서비스 관련 에러 (6000-6999)
    S3_UPLOAD_ERROR = (6000, "파일 업로드 서비스 오류가 발생했습니다.")
    PDF_PROCESSING_ERROR = (6001, "PDF 처리 중 오류가 발생했습니다.")
    AI_PROCESSING_ERROR = (6002, "AI 분석 처리 중 오류가 발생했습니다.")
```

### 에러 전파 체계

```
### 체계적 에러코드 시스템

```python
class ErrorCode(Enum):
    # 공통 에러 (1000-1999)
    UNKNOWN_ERROR = (1000, "알 수 없는 오류가 발생했습니다.")
    VALIDATION_ERROR = (1005, "입력 데이터가 올바르지 않습니다.")
    
    # 사용자 관련 에러 (2000-2999)
    USER_NOT_FOUND = (2000, "사용자를 찾을 수 없습니다.")
    
    # 파일 관련 에러 (3000-3999)
    FILE_TYPE_NOT_SUPPORTED = (3002, "지원하지 않는 파일 형식입니다.")
    
    # 검사 관련 에러 (4000-4999)
    HMT_PROCESSING_ERROR = (4001, "흥미검사 처리 중 오류가 발생했습니다.")
    CST_PROCESSING_ERROR = (4101, "직업적성검사 처리 중 오류가 발생했습니다.")
    
    # 외부 서비스 관련 에러 (6000-6999)
    S3_UPLOAD_ERROR = (6000, "파일 업로드 서비스 오류가 발생했습니다.")
    PDF_PROCESSING_ERROR = (6001, "PDF 처리 중 오류가 발생했습니다.")
    AI_PROCESSING_ERROR = (6002, "AI 분석 처리 중 오류가 발생했습니다.")
```

### 에러 전파 체계

```
PDF 처리 (PdfExtracter) → 비즈니스 로직 (Service) → API (Controller) → 클라이언트
```

### HTTP 상태 코드 매핑

- **400**: 잘못된 요청, 파일 업로드 오류
- **401**: 인증 실패, 토큰 만료
- **403**: 접근 권한 없음
- **404**: 리소스 없음
- **409**: 리소스 충돌
- **413**: 파일 크기 초과
- **422**: 데이터 검증 실패
- **500**: 서버 내부 오류

## 🧪 테스트

### 테스트 실행

```bash
# 전체 테스트
cd Test
python -m pytest

# 특정 테스트
python -m pytest test_hmt.py
python -m pytest test_Cst.py

# 상세 출력
python -m pytest -v
```



## 📄 라이선스

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


