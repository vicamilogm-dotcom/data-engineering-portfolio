from pydantic import BaseModel

__all__ = ["AdditionInputModel", "FibInputModel"]


# Pydantic Query models
class AdditionInputModel(BaseModel):
    a: int
    b: int


class FibInputModel(BaseModel):
    iteration: int
