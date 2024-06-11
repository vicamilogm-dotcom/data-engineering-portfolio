from typing import List

from pydantic import BaseModel


class Settings(BaseModel):
    n_movies: int
    n_comments: int
    movies_fp: str
    comments_fp: str


# Define the models
class Comment(BaseModel):
    movie_id: int
    comment: str
    rating: int


class LatestCommentsResponse(BaseModel):
    comments: List[Comment]
