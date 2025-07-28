from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.HmtController import router as hmt_router
from routes.CstController import router as cst_router
from routes.UserController import router as user_router
from util.exception_handler import setup_exception_handlers
import uvicorn
import logging

# 로깅 설정
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

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(hmt_router, tags=["흥미검사"])
app.include_router(cst_router, tags=["직업적성검사"])
app.include_router(user_router, tags=["사용자"])

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
    from util.exceptions import ErrorCode, raise_file_exception
    raise_file_exception(ErrorCode.PDF_PROCESSING_ERROR, "테스트 에러 메시지입니다.")

if __name__ == "__main__":
    uvicorn.run(
        "run:app",  # app 폴더 안에서 실행될 때의 경로
        host="0.0.0.0",
        port=8081,
        reload=True,
        log_level="debug"  # 더 자세한 로그
    )