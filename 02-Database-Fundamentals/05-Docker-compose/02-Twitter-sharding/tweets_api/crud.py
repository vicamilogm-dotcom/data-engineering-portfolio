from sqlalchemy.orm import Session

from tweets_api import models, schemas

####### Tweets section #######


def read_tweets(db: Session, skip: int = 0, limit: int = 100):
    """Function should return all tweets with a skip and limit param"""
    return db.query(models.Tweet).offset(skip).limit(limit).all()


def create_tweet(db: Session, tweet: schemas.TweetCreate):
    """Function should create a new tweet in the database"""
    db_tweet = models.Tweet(**tweet.model_dump())
    db.add(db_tweet)
    db.commit()
    db.refresh(db_tweet)
    return db_tweet
