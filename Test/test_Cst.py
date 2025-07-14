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
    Base.metadata.create_all(bind=engine)
    yield
    #Base.metadata.drop_all(bind=engine)

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

    uid = str(uuid.uuid4())
    user = User(uid=uid, name="test_user", gradeNum=1)
    sess.add(user)
    sess.commit()
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
    resp: Cst = cstService.createCst(user, upload)
    resp: Cst = cstService.createCst(user, upload)
    csts=cstService.allCstByUser(user)
    print(CstResponse.model_validate(resp))
    print(csts)
