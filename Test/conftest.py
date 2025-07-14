"""
import io
import uuid
import pytest
from pathlib import Path
from fastapi import UploadFile
from sqlalchemy import text

from app.db import engine, SessionLocal
from app.domain.entity.BaseEntity import Base
from app.domain.User import User
import app.domain.User
import app.domain.Hmt
import app.domain.Cst

# ─── 1) 모든 테이블 생성/삭제 (한 세션당 한 번)
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # 테이블 생성
    Base.metadata.create_all(bind=engine)
    yield
    # teardown: FK 검사 끄기 → 테이블 삭제 → FK 검사 켜기
    with engine.connect() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        Base.metadata.drop_all(bind=engine)
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))

# ─── 2) DB 세션 픽스처
@pytest.fixture
def db_session():
    session = SessionLocal()
    yield session
    session.close()

# ─── 3) 테스트 유저 생성 (DetachedInstance 방지용 expunge 포함)
@pytest.fixture
def test_user(db_session):
    generated_uid = str(uuid.uuid4())
    user = User(uid=generated_uid, name="테스트유저", gradeNum=1)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    db_session.expunge(user)
    return user

# ─── 4) real_test.pdf 경로 픽스처
@pytest.fixture
def real_pdf():
    path = Path(__file__).parent / "resorces" / "testHmt.pdf"
    if not path.exists():
        pytest.skip(f"{path}가 없습니다. 테스트를 건너뜁니다.")
    return path

# ─── 5) UploadFile 헬퍼
@pytest.fixture
def upload_file(real_pdf: Path) -> UploadFile:
    buf = io.BytesIO(real_pdf.read_bytes())
    return UploadFile(filename="tests.pdf", file=buf)
"""