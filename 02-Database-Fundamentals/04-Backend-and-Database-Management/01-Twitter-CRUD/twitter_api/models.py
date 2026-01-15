from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)

    # ✅ 1 user -> many tweets
    tweets = relationship(
        "Tweet",
        back_populates="owner",
        cascade="all, delete-orphan",
        order_by="Tweet.id",
    )

    # ✅ 1 user -> many likes
    likes = relationship(
        "Like",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # ✅ many tweets -> 1 owner
    owner = relationship("User", back_populates="tweets")

    # ✅ 1 tweet -> many likes
    likes = relationship(
        "Like",
        back_populates="tweet",
        cascade="all, delete-orphan",
    )


class Like(Base):
    __tablename__ = "likes"

    # ✅ composite PK (user_id + tweet_id)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    tweet_id = Column(Integer, ForeignKey("tweets.id"), primary_key=True)

    # ✅ relations
    user = relationship("User", back_populates="likes")
    tweet = relationship("Tweet", back_populates="likes")
