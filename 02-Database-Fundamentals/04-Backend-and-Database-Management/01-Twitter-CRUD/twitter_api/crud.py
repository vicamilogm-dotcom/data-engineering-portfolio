from sqlalchemy.orm import Session
from fastapi import HTTPException

from twitter_api import models, schemas


# -------------------
# Users
# -------------------
def read_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def read_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def read_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# -------------------
# Tweets
# -------------------
def create_tweet(db: Session, tweet: schemas.TweetCreate, user_id: int):
    db_tweet = models.Tweet(text=tweet.text, owner_id=user_id)
    db.add(db_tweet)
    db.commit()
    db.refresh(db_tweet)
    return db_tweet


def read_tweets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tweet).offset(skip).limit(limit).all()


def read_tweet(db: Session, tweet_id: int):
    return db.query(models.Tweet).filter(models.Tweet.id == tweet_id).first()


# -------------------
# Likes
# -------------------
def create_like(db: Session, user_id: int, tweet_id: int):
    existing = (
        db.query(models.Like)
        .filter(models.Like.user_id == user_id, models.Like.tweet_id == tweet_id)
        .first()
    )
    if existing:
        # ✅ required by tests: duplicate like must raise 400
        raise HTTPException(status_code=400, detail="Like already exists")

    db_like = models.Like(user_id=user_id, tweet_id=tweet_id)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like


def read_user_likes(db: Session, user_id: int):
    return db.query(models.Like).filter(models.Like.user_id == user_id).all()


def read_user_liked_tweets(db: Session, user_id: int):
    return (
        db.query(models.Tweet)
        .join(models.Like, models.Like.tweet_id == models.Tweet.id)
        .filter(models.Like.user_id == user_id)
        .all()
    )
