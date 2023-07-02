from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DB_URL = 'postgresql://postgres:1234@127.0.0.1:5432/postgres'

engine = create_engine(
    SQLALCHEMY_DB_URL
)


# Clsss For creating Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ORM Model
Base = declarative_base()
