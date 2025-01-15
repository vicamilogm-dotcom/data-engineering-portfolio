from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


POSTGRES_DATABASE_URL = os.environ.get("POSTGRES_DATABASE_URL")

engine = create_engine(
    POSTGRES_DATABASE_URL,
    echo=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
