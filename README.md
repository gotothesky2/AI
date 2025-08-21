# 🧠 AI 검사 시스템 API

> **FastAPI 기반의 지능형 진로 적성 검사 및 입학 성적 분석 시스템**
> 
> 흥미검사(HMT)와 직업적성검사(CST)를 AI로 분석하고, 입학 성적 데이터를 자동으로 매핑하여 맞춤형 리포트를 제공하는 종합 REST API 서비스

## 📋 목차

- [프로젝트 개요](#-프로젝트-개요)
- [주요 기능](#-주요-기능)
- [기술 스택](#-기술-스택)
- [프로젝트 구조](#-프로젝트-구조)
- [시작하기](#-시작하기)
- [API 문서](#-api-문서)
- [핵심 아키텍처](#-핵심-아키텍처)
- [성능 최적화](#-성능-최적화)
- [에러 처리](#-에러-처리)
- [테스트](#-테스트)
- [배포](#-배포)

## 🎯 프로젝트 개요

### 🔍 검사 유형

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

### 🚀 핵심 특징
- **AI 기반 분석**: OpenAI GPT-4o를 활용한 맞춤형 리포트 생성
- **PDF 자동 처리**: 검사 결과 PDF에서 점수 자동 추출
- **실시간 분석**: 업로드 즉시 검사 결과 분석 및 저장
- **보안 인증**: JWT + OAuth 통합 인증 시스템
- **클라우드 연동**: AWS S3를 통한 파일 저장 및 관리
- **입학 성적 매핑**: CSV 데이터를 DB와 자동 매핑하여 입학 가능성 분석
- **유사도 기반 검색**: 대학교명과 학과명의 유사도를 통한 정확한 매칭

## 🛠️ 주요 기능

### 📄 PDF 처리 엔진
- **자동 점수 추출**: 검사 결과 PDF에서 정확한 점수 자동 인식
- **파일 검증**: PDF 형식, 페이지 수, 내용 키워드 자동 확인
- **에러 방지**: 잘못된 PDF 업로드 시 적절한 안내 메시지

### 🤖 AI 분석 엔진
- **맞춤형 리포트**: 개인별 검사 결과에 따른 개인화된 분석
- **JSON 응답**: 구조화된 데이터로 일관된 응답 형식
- **토큰 최적화**: 효율적인 GPT API 사용으로 비용 절약

### 🎓 입학 성적 분석 시스템
- **CSV 자동 매핑**: 입학 성적 데이터를 대학교/학과와 자동 연결
- **유사도 검사**: 대학교명과 학과명의 유사도를 통한 정확한 매칭
- **성적 비교**: 사용자 교과 성적과 입학 컷 비교 분석
- **북마크 시스템**: 관심 학과/대학 저장 및 관리

### 🔐 보안 시스템
- **JWT 인증**: 안전한 토큰 기반 인증
- **OAuth 연동**: 소셜 로그인 지원
- **Redis 세션**: 사용자 세션 정보 캐싱
- **권한 관리**: 역할 기반 접근 제어

### 💾 데이터 관리
- **자동 타임스탬프**: 생성/수정 시간 자동 기록
- **관계 매핑**: 사용자-검사 결과 간 효율적인 연관 관계
- **배치 처리**: 대량 데이터 처리 최적화

## 🏗️ 기술 스택

### 🔧 Backend Framework
- **FastAPI 0.116.1**: 현대적이고 빠른 Python 웹 프레임워크
- **Python 3.8+**: 타입 힌트와 최신 Python 기능 활용
- **Uvicorn 0.27.1**: ASGI 서버로 고성능 비동기 처리
- **uvloop 0.21.0**: 이벤트 루프 최적화

### 🗄️ Database & ORM
- **SQLAlchemy 2.0.41**: 최신 ORM으로 타입 안전성 보장
- **MySQL**: 안정적인 관계형 데이터베이스
- **PyMySQL 1.1.1**: Python MySQL 드라이버
- **Redis 6.2.0**: 고성능 인메모리 캐시

### 🤖 AI 
- **OpenAI GPT-4o**: 최신 AI 모델로 정확한 분석
- **PyMuPDF 1.26.3**: PDF 텍스트 추출 및 처리
- **NumPy 2.3.2**: 수치 계산 및 데이터 처리
- **Pandas 2.3.1**: 데이터 분석 및 조작

### ☁️ Cloud & Storage
- **AWS S3**: 확장 가능한 클라우드 스토리지
- **boto3 1.34.44**: AWS SDK for Python
- **python-dotenv 1.1.1**: 환경 변수 관리

### 🔒 Security & Validation
- **PyJWT 2.8.0**: JWT 토큰 생성 및 검증
- **Pydantic 2.11.7**: 데이터 검증 및 직렬화
- **python-multipart 0.0.20**: 파일 업로드 처리

### 🧪 Testing & Development
- **pytest 8.4.1**: Python 테스트 프레임워크
- **Flask 3.1.1**: 개발용 마이크로 프레임워크
- **watchfiles 1.1.0**: 파일 변경 감지

## 📁 프로젝트 구조

```
AI/
├── 📁 app/                          # 메인 애플리케이션
│   ├── 🚀 run.py                   # FastAPI 서버 실행 파일
│   ├── 🗄️ db.py                    # 데이터베이스 연결 설정
│   ├── 📁 domain/                  # 도메인 모델 (엔티티)
│   │   ├── 📁 entity/
│   │   │   └── 🏗️ BaseEntity.py    # 기본 엔티티 (자동 타임스탬프)
│   │   ├── 👤 User.py              # 사용자 엔티티
│   │   ├── 🧠 Hmt.py               # 흥미검사 엔티티
│   │   ├── 🎯 Cst.py               # 직업적성검사 엔티티
│   │   ├── 🤖 AiReport.py          # AI 분석 리포트 엔티티
│   │   ├── 📁 reportModule/        # 리포트 모듈
│   │   │   ├── 📊 Report.py        # 리포트 엔티티
│   │   │   └── 📈 ReportScore.py   # 리포트 점수 엔티티
│   │   ├── 📁 mockModule/          # 모의고사 모듈
│   │   │   ├── 📝 Mock.py          # 모의고사 엔티티
│   │   │   └── 🎯 MockScore.py     # 모의고사 점수 엔티티
│   │   ├── 🎓 Major.py             # 전공 엔티티
│   │   ├── 🌟 Field.py             # 분야 엔티티
│   │   ├── 🏫 University.py        # 대학교 엔티티
│   │   ├── 🔗 UniversityMajor.py   # 대학-전공 연관 엔티티
│   │   ├── 🔐 OAuth.py             # OAuth 인증 엔티티
│   │   ├── 📊 AdmissionScore.py    # 입학 성적 엔티티
│   │   └── 🔖 MajorBookmark.py     # 학과 북마크 엔티티
│   ├── 📁 DTO/                     # 데이터 전송 객체
│   │   ├── 🧠 HmtDTO.py            # 흥미검사 DTO
│   │   ├── 🎯 CstDTO.py            # 직업적성검사 DTO
│   │   ├── 👤 UserDTO.py           # 사용자 DTO
│   │   └── 🤖 AiRepotDto.py        # AI 리포트 DTO
│   ├── 📁 repository/               # 데이터 접근 계층
│   │   ├── 🏗️ Repository.py        # 기본 레포지토리 (CRUD 공통 로직)
│   │   ├── 👤 userRepository.py    # 사용자 레포지토리
│   │   ├── 🧠 hmtRepository.py     # 흥미검사 레포지토리
│   │   ├── 🎯 cstRepository.py     # 직업적성검사 레포지토리
│   │   ├── 🤖 aiReportRepository.py # AI 리포트 레포지토리
│   │   ├── 📊 reportRepository.py  # 리포트 레포지토리
│   │   ├── 📝 mockRepository.py    # 모의고사 레포지토리
│   │   ├── 🎓 majorRepository.py   # 전공 레포지토리
│   │   ├── 🌟 fieldRepository.py   # 분야 레포지토리
│   │   ├── 🏫 universityRepository.py # 대학교 레포지토리
│   │   ├── 🔐 oauthRepository.py   # OAuth 레포지토리
│   │   └── 📊 admissionScoreRepository.py # 입학 성적 레포지토리
│   ├── 📁 services/                 # 비즈니스 로직 계층
│   │   ├── 🧠 HmtService.py        # 흥미검사 서비스
│   │   ├── 🎯 CstService.py        # 직업적성검사 서비스
│   │   ├── 👤 UserService.py       # 사용자 서비스
│   │   ├── 🤖 AiReportService.py   # AI 리포트 서비스
│   │   └── 📊 ExcelMappingService.py # Excel 매핑 서비스
│   ├── 📁 routes/                   # API 라우터 (컨트롤러)
│   │   ├── 🧠 HmtController.py     # 흥미검사 컨트롤러
│   │   ├── 🎯 CstController.py     # 직업적성검사 컨트롤러
│   │   ├── 🔐 AuthController.py    # 인증 컨트롤러
│   │   └── 🤖 AiReportController.py # AI 리포트 컨트롤러
│   ├── 📁 login/                    # 인증 시스템
│   │   ├── 🔐 jwt_auth.py          # JWT 인증 서비스
│   │   ├── 🛠️ jwt_util.py          # JWT 유틸리티
│   │   ├── 🌐 oauth_jwt_auth.py    # OAuth + JWT 통합 인증
│   │   ├── 🗄️ redis_auth.py        # Redis 인증
│   │   └── 👤 jwtUser.py           # JWT 사용자 모델
│   ├── 📁 gptApi/                   # GPT API 연동
│   │   ├── 🧠 gptEngine.py         # GPT 엔진 (추상 클래스)
│   │   ├── 📊 testReportEng/       # 테스트 리포트 엔진
│   │   │   └── 📈 testReport.py    # 테스트 리포트 생성
│   │   └── 🧪 test.py              # GPT API 테스트
│   ├── 📁 util/                     # 유틸리티
│   │   ├── 🔄 Transactional.py     # 트랜잭션 데코레이터 (읽기/쓰기 분리)
│   │   ├── 📁 globalDB/            # 글로벌 DB 컨텍스트
│   │   │   ├── 🔗 db_context.py    # DB 컨텍스트 관리
│   │   │   └── 🌐 global_db.py     # 글로벌 DB 접근
│   │   ├── 📁 PdfExtracter/        # PDF 처리 엔진
│   │   │   ├── 🧠 HmtExtracter.py  # 흥미검사 PDF 분석
│   │   │   └── 🎯 CstExtracter.py  # 직업적성검사 PDF 분석
│   │   ├── 📁 S3/                  # AWS S3 연동
│   │   │   └── ☁️ S3_Util.py       # S3 파일 업로드/다운로드
│   │   ├── 🔐 auth_dependency.py   # 인증 의존성
│   │   ├── 📅 termGenerator.py     # 학기 생성기
│   │   ├── 🔍 similarity_checker.py # 유사도 검사 유틸리티
│   │   └── 📊 GradeComparisonUtil.py # 성적 비교 유틸리티
│   ├── 📁 globals/                  # 전역 설정
│   │   ├── 🚨 exceptions.py        # 커스텀 예외 및 에러코드
│   │   ├── 🛡️ exception_handler.py # 전역 예외 처리기
│   │   └── 📋 error_codes.md       # 에러코드 문서
│   ├── 📁 mappingProgram/           # 데이터 매핑 프로그램
│   │   ├── 🔄 remap_with_similarity.py # 유사도 기반 재매핑
│   │   ├── 📊 show_db_data.py      # DB 데이터 조회
│   │   └── 🔍 show_unmapped_combinations.py # 미매핑 조합 조회
│   ├── 🗄️ redisClient.py           # Redis 클라이언트
│   ├── 📊 교과 데이터.csv            # 입학 성적 CSV 데이터
│   ├── 📈 입학성적_전체데이터.csv     # 전체 입학 성적 데이터
│   └── __init__.py
├── 📁 Test/                         # 테스트 코드
├── 📁 PdfExtractor/                 # PDF 추출 테스트
├── 🧪 pytest.ini                   # pytest 설정
├── 📦 requirements.txt              # Python 의존성
├── 🚀 ai-api.service               # 시스템 서비스 파일
└── 📖 README.md                     # 프로젝트 문서
```

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
# GPT API 설정
GPT_API_KEY=your_openai_api_key_here

# 데이터베이스 선택 (LOCAL 또는 AWS)
DB_SELECT=LOCAL

# 로컬 데이터베이스 설정
LOCAL_HOST=localhost
LOCAL_USER=your_username
LOCAL_PASSWORD=your_password
LOCAL_PORT=3306
LOCAL_NAME=your_database_name

# AWS RDS 데이터베이스 설정
AWS_USER=your_aws_username
AWS_PASSWORD=your_aws_password
AWS_ADDRESS=your_aws_endpoint
AWS_NAME=your_aws_database_name
AWS_PORT=3306

# AWS S3 설정
AWS_S3_BUCKET_NAME=your_s3_bucket_name
AWS_S3_ACCESS_KEY=your_s3_access_key
AWS_S3_SECRET_KEY=your_s3_secret_key

# JWT 설정
JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_EXPIRATION=3600          # 액세스 토큰 만료 시간 (초)
JWT_REFRESH_EXPIRATION=86400 # 리프레시 토큰 만료 시간 (초)

# Redis 설정
REDIS_HOST=localhost
REDIS_PORT=6379
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

### 🤖 AI 리포트 API

#### POST /ai-report
검사 결과를 기반으로 AI 분석 리포트를 생성합니다.

#### GET /ai-report/my
현재 사용자의 모든 AI 리포트를 조회합니다.

### 🧪 테스트 API

#### GET /test-error
예외 처리 테스트용 엔드포인트

#### GET /health
서버 상태 확인

## 🏗️ 핵심 아키텍처

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
- **토큰 제한**: 10000
- **온도**: 0.6 (창의성과 일관성의 균형)

#### 구현체
- **TestReportEngine**: 테스트 결과 기반 맞춤형 리포트 생성

### 🎓 입학 성적 분석 시스템

#### ExcelMappingService
- **CSV 자동 매핑**: 입학 성적 데이터를 대학교/학과와 자동 연결
- **유사도 기반 매칭**: 대학교명과 학과명의 유사도를 통한매칭
- **데이터 검증**: 성적 데이터의 유효성 검사 및 보정

#### SimilarityChecker
- **대학교명 매칭**: 별칭, 캠퍼스명 등을 고려한 매칭
- **학과명 매칭**: 유사도 기반 퍼지 매칭
- **별칭 사전**: 주요 대학교의 일반적인 별칭 관리

#### GradeComparisonUtil
- **교과 성적 분석**: 사용자별 과목별 평균 등급 계산
- **입학 가능성 분석**: 사용자 성적과 입학 컷 비교
- **북마크 연동**: 관심 학과/대학과의 성적 비교

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
- **User ↔ Report**: 1:N (사용자당 여러 교과 성적)
- **User ↔ MajorBookmark**: 1:N (사용자당 여러 학과 북마크)
- **University ↔ Major**: M:N (대학교-학과 다대다 관계)

### 🔄 트랜잭션 관리

#### Transactional 데코레이터
- **@Transactional**: 기본 트랜잭션 (자동 커밋)
- **@TransactionalRead**: 읽기 전용 (커밋 없음)
- **@TransactionalWrite**: 쓰기 전용 (명시적 커밋)

## ⚡ 성능 최적화

### 🚀 데이터베이스 최적화

#### Repository 패턴 개선
- **flush_immediately 옵션**: 선택적 DB 동기화로 성능 향상
- **save_all() 메서드**: 배치 삽입으로 대량 데이터 처리 최적화
- **연결 풀 최적화**: pool_size=20, max_overflow=30 설정

#### 트랜잭션 최적화
- **읽기/쓰기 분리**: 불필요한 커밋 오버헤드 제거
- **배치 처리**: 대량 데이터 처리 시 성능 향상


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

# 커버리지 확인
python -m pytest --cov=app
```

### 테스트 구조
- **단위 테스트**: 개별 함수/클래스 테스트
- **통합 테스트**: API 엔드포인트 테스트
- **PDF 처리 테스트**: 파일 업로드 및 분석 테스트



### 환경별 설정

#### 개발 환경
- `DB_SELECT=LOCAL`
- `echo=True` (SQL 로깅)
- `debug=True`

#### 프로덕션 환경
- `DB_SELECT=AWS`
- `echo=False`
- `debug=False`
- 환경 변수 보안 강화

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해 주세요.

---

**⭐ 이 프로젝트가 도움이 되었다면 스타를 눌러주세요!**


