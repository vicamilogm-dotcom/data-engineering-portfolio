import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DB_URL = os.environ.get("POSTGRES_DATABASE_URL")
engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if __name__ == "__main__":
    query = text(
        """
        SELECT * FROM information_schema.tables
        WHERE table_schema = 'public'
    """
    )
    with SessionLocal() as db:
        print(db.execute(query).fetchall())
