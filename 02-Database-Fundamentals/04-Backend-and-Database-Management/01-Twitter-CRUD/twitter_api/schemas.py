from pydantic import BaseModel, ConfigDict

# User section


class UserBase(BaseModel):
    pass  # YOUR CODE HERE


class UserCreate(UserBase):
    pass  # YOUR CODE HERE


class User(UserBase):
    pass  # YOUR CODE HERE


# Tweet section


class TweetBase(BaseModel):
    pass  # YOUR CODE HERE


class TweetCreate(TweetBase):
    pass  # YOUR CODE HERE


class Tweet(TweetBase):
    pass  # YOUR CODE HERE


# Like section


class LikeBase(BaseModel):
    pass  # YOUR CODE HERE


class LikeCreate(LikeBase):
    pass  # YOUR CODE HERE


class Like(LikeBase):
    pass  # YOUR CODE HERE
