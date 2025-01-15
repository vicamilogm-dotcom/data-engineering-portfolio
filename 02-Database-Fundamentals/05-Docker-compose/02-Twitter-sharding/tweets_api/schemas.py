from pydantic import BaseModel, ConfigDict

# Tweet section


class TweetBase(BaseModel):
    text: str


class TweetCreate(TweetBase):
    owner_id: int
    location: str
    like_count: int


class Tweet(TweetBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
