# Part 1

# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"App":"Running!"}


# Part 2
# Don't forget to create a .envrc and .env

from sqlalchemy import create_engine, text
from fastapi import FastAPI
import os

app = FastAPI()

SQLALCHEMY_DATABASE_URL = os.environ.get("DB_URL")


@app.get("/")
def read_root():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
    query = text("SELECT 1")
    with engine.connect() as conn:
        result = conn.execute(query).fetchone()[0]
    return {"DB": str(result)}
