from pydantic import BaseModel, ConfigDict

# User section


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    model_config = ConfigDict(coerce_numbers_to_str=True)


# Tweet section


class TweetBase(BaseModel):
    text: str


class TweetCreate(TweetBase):
    pass


class Tweet(TweetBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


# Like section


class LikeBase(BaseModel):
    tweet_id: int


class LikeCreate(LikeBase):
    pass


class Like(LikeBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
