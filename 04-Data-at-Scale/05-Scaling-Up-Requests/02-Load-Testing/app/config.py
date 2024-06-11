from pydantic import BaseSettings

__all__ = [
    "Settings",
]


class Settings(BaseSettings):
    pass  # YOUR CODE HERE


if __name__ == "__main__":
    settings = Settings()
