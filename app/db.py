from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:gaga2430@localhost:3306/@localhost"
engine = create_engine(DATABASE_URL,
                       echo=True,
                       pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)
