from pydantic import BaseModel, ConfigDict


# -------------------
# Users
# -------------------
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# -------------------
# Tweets
# -------------------
class TweetBase(BaseModel):
    text: str


class TweetCreate(TweetBase):
    pass


class Tweet(TweetBase):
    id: int
    owner_id: int
    model_config = ConfigDict(from_attributes=True)


# -------------------
# Likes
# -------------------
class LikeCreate(BaseModel):
    tweet_id: int


class Like(BaseModel):
    user_id: int
    tweet_id: int
    model_config = ConfigDict(from_attributes=True)
