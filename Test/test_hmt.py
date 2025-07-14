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
from app.services.HmtService  import hmtService
from app.DTO.HmtDTO           import HmtResponse
from app.util.PdfExtracter.HmtExtracter import HmtExtracter

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
def test_create_hmt_commits(test_user, monkeypatch):
    user, sess = test_user

    # SessionLocal() 호출을 항상 동일한 sess로 리턴하도록 패치
    import app.db as db_mod
    monkeypatch.setattr(db_mod, "SessionLocal", lambda: sess)

    # S3 업로드 더미
    hmtService._s3 = type("S3Dummy", (), {
        "upload_bytes": lambda self, b, k: f"https://fake/{k}"
    })()

    # PDF 준비
    pdf_path = Path(__file__).parent / "resorces" / "testHmt.pdf"
    upload = make_uploadfile(pdf_path)

    # 실행 & 검증
    resp:Hmt = hmtService.createHmt(user, upload)
    resp: Hmt = hmtService.createHmt(user, upload)
    hmts=hmtService.allHmtByUserId(user)
    print(HmtResponse.model_validate(resp))
    print(hmts)

# ————————————————
# 6) 예외 시 롤백 테스트
# ————————————————

"""
def test_create_hmt_rolls_back_on_error(test_user, monkeypatch):
    user, sess = test_user

    # 같은 방식으로 세션 패치
    import app.db as db_mod
    monkeypatch.setattr(db_mod, "SessionLocal", lambda: sess)

    # HmtExtracter 강제 에러
    original_new = HmtExtracter.__new__
    HmtExtracter.__new__ = staticmethod(lambda cls, f: (_ for _ in ()).throw(ValueError("parse fail")))

    # S3 더미 유지
    hmtService._s3 = type("S3Dummy", (), {
        "upload_bytes": lambda self, b, k: f"https://fake/{k}"
    })()

    pdf_path = Path(__file__).parent / "resorces" / "testHmt.pdf"
    upload = make_uploadfile(pdf_path)

    # 예외 및 롤백 확인
    with pytest.raises(ValueError):
        test=hmtService.createHmt(user, upload)
        print(test.model_dump_json(by_alias=True))

    # 복원
    HmtExtracter.__new__ = original_new

"""
