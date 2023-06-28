from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DB_URL = 'mysql://root:1234@localhost:3306/board'

engine = create_engine(
    SQLALCHEMY_DB_URL
)


#Clsss For creating Session
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)


#ORM Model
Base = declarative_base()