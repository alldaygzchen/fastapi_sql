from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABABE_URL = 'postgresql://postgres:gonzalo0000@localhost/fastapi'
engine = create_engine(SQLALCHEMY_DATABABE_URL) #establish connection
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
