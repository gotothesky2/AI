# AI 검사 시스템 API

흥미검사(HMT)와 직업적성검사(CST)를 위한 FastAPI 기반 REST API 시스템입니다.

## 🚀 주요 기능

### 📋 흥미검사 (HMT - Holland's Theory)
- PDF 파일 업로드 및 분석
- RIASEC 모델 기반 흥미 영역 점수 산출 (R, I, A, S, E, C)
- 개인별 흥미 프로파일 생성

### 👔 직업적성검사 (CST - Career Skills Test)
- PDF 파일 업로드 및 분석
- 11개 능력영역별 점수 측정
  - 수리·논리력, 예술시각능력, 손재능, 공간지각력, 음악능력
  - 대인관계능력, 창의력, 언어능력, 신체·운동능력, 자연친화력, 자기성찰능력

### 👤 사용자 관리
- Spring Boot 백엔드와 연동된 사용자 정보
- 검사 이력 관리

## 🛠 기술 스택

- **Backend**: FastAPI, SQLAlchemy, Python 3.8+
- **Database**: MySQL (Spring Boot와 공유)
- **Storage**: AWS S3 (Mock 구현)
- **AI**: GPT API 기반 분석
- **PDF Processing**: PyMuPDF (fitz)

## 📁 프로젝트 구조

```
AI/
├── app/                          # 메인 애플리케이션
│   ├── run.py                   # FastAPI 서버 실행 파일
│   ├── db.py                    # 데이터베이스 설정
│   ├── domain/                  # 도메인 모델
│   │   ├── entity/
│   │   │   └── BaseEntity.py
│   │   ├── User.py             # 사용자 엔티티
│   │   ├── Hmt.py              # 흥미검사 엔티티
│   │   └── Cst.py              # 직업적성검사 엔티티
│   ├── DTO/                     # 데이터 전송 객체
│   │   ├── HmtDTO.py
│   │   └── CstDTO.py
│   ├── repository/              # 데이터 접근 계층
│   │   ├── Repository.py        # 기본 레포지토리
│   │   ├── userRepository.py
│   │   ├── hmtRepository.py
│   │   └── cstRepository.py
│   ├── services/                # 비즈니스 로직
│   │   ├── HmtService.py
│   │   └── CstService.py
│   ├── routes/                  # API 라우터
│   │   ├── HmtController.py
│   │   ├── CstController.py
│   │   └── UserController.py
│   └── util/                    # 유틸리티
│       ├── Transactional.py     # 트랜잭션 데코레이터
│       ├── exceptions.py        # 커스텀 예외
│       ├── exception_handler.py # 예외 처리기
│       ├── PdfExtracter/        # PDF 처리
│       │   ├── HmtExtracter.py
│       │   └── CstExtracter.py
│       └── globalDB/            # 글로벌 DB 컨텍스트
├── Test/                        # 테스트 코드
└── requirements.txt             # Python 의존성
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

### 2. 데이터베이스 설정

MySQL 데이터베이스 연결 정보를 `app/db.py`에서 설정하세요:

```python
DATABASE_URL = "mysql+pymysql://username:password@localhost:3306/database_name"
```

### 3. 서버 실행

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

### 흥미검사 API

#### POST /hmt
흥미검사 PDF 파일을 업로드하여 분석합니다.

**요청**:
- `file`: PDF 파일 (multipart/form-data)
- `user_id`: 사용자 ID (query parameter)

**응답**:
```json
{
  "success": true,
  "message": "흥미검사가 성공적으로 생성되었습니다.",
  "data": {
    "id": 1,
    "uid": "user-uuid",
    "pdfLink": "https://s3-url/file.pdf",
    "hmtGradeNum": 1,
    "hmtTermNum": 2,
    "uploadTime": "2024-01-15T10:30:00",
    "rScore": 85.5,
    "iScore": 90.0,
    "aScore": 78.3,
    "sScore": 82.1,
    "eScore": 88.7,
    "cScore": 75.9
  }
}
```

#### GET /hmt/{hmt_id}
특정 흥미검사 결과를 조회합니다.

#### GET /hmt/user/{user_id}
사용자별 흥미검사 목록을 조회합니다.

#### DELETE /hmt/{hmt_id}
흥미검사 결과를 삭제합니다.

### 직업적성검사 API

#### POST /cst
직업적성검사 PDF 파일을 업로드하여 분석합니다.

**요청**:
- `file`: PDF 파일 (multipart/form-data)
- `user_id`: 사용자 ID (query parameter)

**응답**:
```json
{
  "success": true,
  "message": "직업적성검사가 성공적으로 생성되었습니다.",
  "data": {
    "id": 1,
    "uid": "user-uuid",
    "pdfLink": "https://s3-url/file.pdf",
    "cstGradeNum": 1,
    "cstTermNum": 2,
    "uploadTime": "2024-01-15T10:30:00",
    "mathScore": 85.5,
    "artScore": 90.0,
    "handScore": 78.3,
    "spaceScore": 82.1,
    "musicScore": 88.7,
    "relationScore": 75.9,
    "creativeScore": 87.2,
    "langScore": 91.3,
    "physicalScore": 76.8,
    "natureScore": 84.6,
    "selfScore": 89.1
  }
}
```

#### GET /cst/{cst_id}
특정 직업적성검사 결과를 조회합니다.

#### GET /cst/user/{user_id}
사용자별 직업적성검사 목록을 조회합니다.

#### DELETE /cst/{cst_id}
직업적성검사 결과를 삭제합니다.

## 🔧 에러 처리

시스템은 체계적인 에러코드를 사용합니다:

### 에러 응답 형식
```json
{
  "success": false,
  "error": {
    "error_code": 6001,
    "error_message": "PDF 처리 중 오류가 발생했습니다.",
    "error_type": "PDF_PROCESSING_ERROR"
  },
  "path": "http://localhost:8081/hmt",
  "method": "POST"
}
```

### 주요 에러코드
- **1000-1999**: 공통 에러 (UNKNOWN_ERROR, VALIDATION_ERROR 등)
- **2000-2999**: 사용자 관련 에러 (USER_NOT_FOUND 등)
- **3000-3999**: 파일 관련 에러 (FILE_TYPE_NOT_SUPPORTED 등)
- **4000-4999**: 검사 관련 에러 (HMT_PROCESSING_ERROR, CST_PROCESSING_ERROR 등)
- **5000-5999**: 데이터베이스 관련 에러
- **6000-6999**: 외부 서비스 관련 에러 (S3_UPLOAD_ERROR, PDF_PROCESSING_ERROR 등)

## 🧪 테스트

```bash
# 테스트 실행
cd Test
python -m pytest

# 특정 테스트 실행
python -m pytest test_hmt.py
python -m pytest test_Cst.py
```

### 테스트용 엔드포인트
- **GET /test-error**: 예외 처리 테스트용 엔드포인트

## 🔄 Spring Boot 연동

이 시스템은 기존 Spring Boot 애플리케이션과 MySQL 데이터베이스를 공유합니다:

- **User 테이블**: Spring Boot에서 관리 (읽기 전용)
- **Hmt, Cst 테이블**: Python에서 관리 (생성/삭제 가능)
- **공유 데이터베이스**: 동일한 MySQL 인스턴스 사용

## 📝 개발 참고사항

### Spring-like 트랜잭션 처리
```python
@Transactional
def createHmt(self, user_id: str, file: UploadFile):
    # 자동으로 트랜잭션 시작
    # 메서드 완료 시 자동 커밋
    # 예외 발생 시 자동 롤백
```

### 에러 전파 시스템
```
유틸단 (PdfExtracter) → 서비스단 (Service) → 라우트단 (Controller) → 클라이언트
```

### 성능 최적화 기록
[[memory:3657103]]에 기록된 성능 최적화 방안들이 있으며, 추후 검토 후 적용 예정입니다.

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.