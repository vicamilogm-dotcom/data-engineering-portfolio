from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from twitter_api import crud, schemas
from twitter_api.database import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Le Wagon Twitter app": "Running"}


# -------------------
# Users
# -------------------
@app.post("/users/", response_model=schemas.User, tags=["users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.read_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User], tags=["users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.read_users(db, skip=skip, limit=limit)


@app.get("/users/{user_id}", response_model=schemas.User, tags=["users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.read_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# -------------------
# Tweets
# -------------------
@app.post("/users/{user_id}/tweets/", response_model=schemas.Tweet, tags=["tweets"])
def create_tweet(user_id: int, tweet: schemas.TweetCreate, db: Session = Depends(get_db)):
    db_user = crud.read_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_tweet(db=db, tweet=tweet, user_id=user_id)


@app.get("/users/{user_id}/tweets/", response_model=list[schemas.Tweet], tags=["tweets"])
def read_user_tweets(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.read_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user.tweets


@app.get("/tweets/", response_model=list[schemas.Tweet], tags=["tweets"])
def read_tweets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.read_tweets(db, skip=skip, limit=limit)


# -------------------
# Likes
# -------------------
@app.post("/users/{user_id}/likes/", response_model=schemas.Like, tags=["likes"])
def create_like(user_id: int, like: schemas.LikeCreate, db: Session = Depends(get_db)):
    if crud.read_user(db, user_id=user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")

    if crud.read_tweet(db, tweet_id=like.tweet_id) is None:
        raise HTTPException(status_code=404, detail="Tweet not found")

    return crud.create_like(db=db, user_id=user_id, tweet_id=like.tweet_id)


@app.get("/users/{user_id}/likes/", response_model=list[schemas.Like], tags=["likes"])
def read_user_likes(user_id: int, db: Session = Depends(get_db)):
    if crud.read_user(db, user_id=user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.read_user_likes(db=db, user_id=user_id)


@app.get("/users/{user_id}/liked_tweets/", response_model=list[schemas.Tweet], tags=["likes"])
def read_user_liked_tweets(user_id: int, db: Session = Depends(get_db)):
    if crud.read_user(db, user_id=user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.read_user_liked_tweets(db=db, user_id=user_id)
