# AI 검사 시스템 API

흥미검사(HMT)와 창의성검사(CST)를 위한 FastAPI 기반 REST API 서버입니다.

## 주요 기능

- **흥미검사 (HMT)**: Holland 이론 기반 흥미 검사 결과 분석
- **창의성검사 (CST)**: 창의성 관련 능력 검사 결과 분석  
- **사용자 관리**: 사용자 등록, 조회, 수정, 삭제
- **PDF 파일 처리**: PDF 업로드 및 자동 분석

## 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 설정
데이터베이스 연결 정보를 설정하세요.

### 3. 서버 실행
```bash
python run.py
```

또는 uvicorn 직접 실행:
```bash
uvicorn run:app --host 0.0.0.0 --port 8000 --reload
```

## API 엔드포인트

### 루트
- `GET /` - API 정보
- `GET /health` - 헬스 체크

### 사용자 관리 (`/users`)
- `POST /users` - 사용자 생성
- `GET /users/{uid}` - 사용자 조회
- `GET /users/email/{email}` - 이메일로 사용자 조회
- `GET /users` - 모든 사용자 조회
- `PUT /users/{uid}` - 사용자 정보 수정
- `DELETE /users/{uid}` - 사용자 삭제
- `PATCH /users/{uid}/token` - 토큰 업데이트

### 흥미검사 (`/hmt`)
- `POST /hmt` - 흥미검사 생성 (PDF 업로드)
- `GET /hmt/{hmt_id}` - 흥미검사 조회
- `GET /hmt/user/{user_id}` - 사용자별 흥미검사 목록
- `DELETE /hmt/{hmt_id}` - 흥미검사 삭제

### 창의성검사 (`/cst`)
- `POST /cst` - 창의성검사 생성 (PDF 업로드)
- `GET /cst/{cst_id}` - 창의성검사 조회
- `GET /cst/user/{user_id}` - 사용자별 창의성검사 목록
- `DELETE /cst/{cst_id}` - 창의성검사 삭제

## API 문서

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 개발 환경

- Python 3.8+
- FastAPI
- SQLAlchemy
- MySQL
- PyMuPDF (PDF 처리)