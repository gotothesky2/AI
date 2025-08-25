from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes.HmtController import router as hmt_router
from routes.CstController import router as cst_router
from routes.AuthController import router as auth_router
from routes.AiReportController import router as ai_report_router
from routes.AdmissionPossibilityController import router as admission_possibility_router
from globals import setup_exception_handlers
from util.globalDB.db_context import set_db, reset_db
from db import SessionLocal,engine
from domain import *
import uvicorn
import logging


def init_database():
    """데이터베이스 초기화 - 모든 테이블 생성"""
    try:
        from domain.entity.BaseEntity import Base
        Base.metadata.create_all(engine, checkfirst=True)
        print("✅ 데이터베이스 초기화 완료!")

        # 등록된 테이블 확인
        registered_tables = list(Base.metadata.tables.keys())
        print(f"📊 등록된 테이블들: {registered_tables}")

    except Exception as e:
        print(f"❌ 데이터베이스 초기화 실패: {e}")
        import traceback
        traceback.print_exc()


init_database()
logging.basicConfig(level=logging.DEBUG)

# FastAPI 앱 생성
app = FastAPI(
    title="AI 검사 시스템 API",
    description="흥미검사(HMT)와 직업적성검사(CST)를 위한 REST API",
    version="1.0.0",
    debug=True  # 디버그 모드 활성화
)

# 전역 예외 처리 설정
setup_exception_handlers(app)

# 데이터베이스 미들웨어 추가
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    """각 요청마다 데이터베이스 세션을 생성하고 관리하는 미들웨어"""
    db = SessionLocal()
    token = set_db(db)
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
        reset_db(token)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth_router, tags=["인증"])
app.include_router(hmt_router, tags=["흥미검사"])
app.include_router(cst_router, tags=["직업적성검사"])

app.include_router(ai_report_router,tags=["ai레포트"])
app.include_router(admission_possibility_router, tags=["합격가능성"])

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {"message": "AI 검사 시스템 API에 오신 것을 환영합니다!"}

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy", "message": "서버가 정상적으로 작동 중입니다."}

@app.get("/test-error")
async def test_error():
    """예외 처리 테스트 엔드포인트"""
    from globals import ErrorCode, raise_file_exception
    raise_file_exception(ErrorCode.PDF_PROCESSING_ERROR, "테스트 에러 메시지입니다.")

if __name__ == "__main__":
    uvicorn.run(
        "run:app",  # app 폴더 안에서 실행될 때의 경로
        host="0.0.0.0",
        port=8081,
        reload=True,
        ssl_keyfile="../127.0.0.1+1-key.pem",  # 개인키 파일 경로
        ssl_certfile="../127.0.0.1.pem",        # 인증서 파일 경로
        log_level="debug"  # 더 자세한 로그
    )