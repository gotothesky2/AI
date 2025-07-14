from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://test1:1q2w3e4r@localhost:3306/Test"
engine = create_engine(DATABASE_URL,
                       echo=True,
                       pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False,expire_on_commit=False,bind=engine)
