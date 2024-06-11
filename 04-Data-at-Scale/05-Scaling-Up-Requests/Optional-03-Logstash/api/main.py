from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from .database import SessionLocal

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root(db: Session = Depends(get_db)):
    return {"running": True}


@app.get("/load-table")
def load_table(table_name: str, db: Session = Depends(get_db)):
    res = db.execute(f"SELECT * FROM {table_name} LIMIT 100")
    if res:
        return {"data": res.fetchall()}
    else:
        return {"DB Status: ERROR"}
