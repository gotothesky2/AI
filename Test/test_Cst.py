"""
import io
import pytest
import uuid
from pathlib import Path
from fastapi import UploadFile
from starlette.datastructures import Headers
from sqlalchemy.orm import Session

from app.db                   import engine, SessionLocal
from app.domain.entity.BaseEntity import Base
from app.domain.User          import User
from app.domain.Hmt           import Hmt
from app.domain.Cst           import Cst
from app.services.CstService  import cstService
from app.DTO.CstDTO import CstResponse
from app.util.PdfExtracter.CstExtracter import CstExtracter

# ————————————————
# 1) 테스트 DB 스키마 초기화
# ————————————————
@pytest.fixture(scope="session", autouse=True)
def init_db():
    # 🚨 Spring 테이블 보존 - 자동 생성 비활성화
    # Base.metadata.create_all(bind=engine)  # 주석 처리
    print("📌 Using existing Spring database tables")
    yield
    # 테이블 삭제도 비활성화 - Spring 데이터 보존
    # Base.metadata.drop_all(bind=engine)

# ————————————————
# 2) 각 테스트 전 테이블 초기화
# ————————————————
@pytest.fixture(autouse=True)
def clear_tables():
    sess = SessionLocal()
    sess.execute(Hmt.__table__.delete())
    sess.execute(Cst.__table__.delete())
    sess.execute(User.__table__.delete())

    sess.commit()
    sess.close()
# ————————————————
# 3) 테스트 유저 생성 (UUID 중복 방지)
# ————————————————
@pytest.fixture
def test_user():
    sess: Session = SessionLocal()
    sess.query(User).delete()
    sess.commit()

    # 기존 Spring DB 테이블들 사용 (테이블 생성 불필요)

    # 기존 Spring DB에 있는 사용자 조회
    existing_uid = "cfd0861b-ff87-48e3-8755-6ad68e5232c5"
    user = sess.query(User).filter(User.uid == existing_uid).first()
    if not user:
        pytest.skip(f"테스트 사용자 {existing_uid}가 DB에 존재하지 않습니다.")
    sess.refresh(user)
    # 세션에서 분리(detach)해두면 이후 attach 시 InvalidRequestError 방지
   # sess.expunge(user)

    yield user.uid, sess

    sess.close()
# ————————————————
# 4) UploadFile 헬퍼
# ————————————————
def make_uploadfile(pdf_path: Path) -> UploadFile:
    data = pdf_path.read_bytes()
    buf = io.BytesIO(data)
    headers = Headers({"content-type": "application/pdf"})
    return UploadFile(filename=pdf_path.name, file=buf, headers=headers)

# ————————————————
# 5) 정상 커밋 테스트
# ————————————————
def test_create_cst_commits(test_user, monkeypatch):
    user, sess = test_user

    # SessionLocal() 호출을 항상 동일한 sess로 리턴하도록 패치
    import app.db as db_mod
    monkeypatch.setattr(db_mod, "SessionLocal", lambda: sess)

    # S3 업로드 더미
    cstService._s3 = type("S3Dummy", (), {
        "upload_bytes": lambda self, b, k: f"https://fake/{k}"
    })()

    # PDF 준비
    pdf_path = Path(__file__).parent / "resorces" / "testCst.pdf"
    upload = make_uploadfile(pdf_path)

    # 실행 & 검증
    resp: CstResponse = cstService.createCst(user, upload)
    resp2: CstResponse = cstService.createCst(user, upload)
    csts = cstService.allCstByUser(user)
    print(resp)
    print(csts)
"""