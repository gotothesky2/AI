from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()

if os.getenv("DB_SELECT") == "AWS":
    DB_HOST = os.getenv("AWS_ADDRESS")
    DB_USER = os.getenv("AWS_USER")
    DB_PASSWORD = os.getenv("AWS_PASSWORD")
    DB_NAME = os.getenv("AWS_NAME")
    DB_PORT = int(os.getenv("AWS_PORT"))
    echo=False


elif os.getenv("DB_SELECT") == "LOCAL":
    DB_HOST = os.getenv("LOCAL_HOST")
    DB_USER = os.getenv("LOCAL_USER")
    DB_PASSWORD = os.getenv("LOCAL_PASSWORD")
    DB_NAME = os.getenv("LOCAL_NAME")
    DB_PORT = int(os.getenv("LOCAL_PORT"))
    echo=True

else:
    raise ValueError("Invalid DB_SELECT")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL,
                       echo=echo,
                       pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False,expire_on_commit=False,bind=engine)
