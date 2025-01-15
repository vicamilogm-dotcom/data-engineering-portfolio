from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from twitter_api.models import Base
from twitter_api.main import app, get_db
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:////tmp/test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Le Wagon Twitter app": "Running"}


@pytest.mark.users
def test_create_user():
    response = client.post("/users/", json={"email": "test@test", "password": "123"})
    assert response.status_code == 200
    response = client.post("/users/", json={"email": "test@test", "password": "123"})
    assert response.status_code == 400


@pytest.mark.users
def test_read_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert list(response.json()[0].keys()) == ["email", "id"]


@pytest.mark.users
def test_read_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert list(response.json().keys()) == ["email", "id"]


@pytest.mark.tweets
def test_create_tweet():
    response = client.post("/users/1/tweets/", json={"text": "test"})
    assert response.status_code == 200


@pytest.mark.tweets
def test_read_tweets():
    response = client.get("/tweets/")
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.tweets
def test_read_user_tweets():
    response = client.get("/users/1/tweets/")
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.likes
def test_create_like():
    response = client.post("/users/1/likes/", json={"tweet_id": 1})
    assert response.status_code == 200
    response = client.post("/users/1/likes/", json={"tweet_id": 1})
    assert response.status_code == 400


@pytest.mark.likes
def test_read_users_likes():
    response = client.get("/users/1/likes/")
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.likes
def test_read_users_likedtweets():
    response = client.get("/users/1/liked_tweets/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    tweets = client.get("/tweets/").json()
    assert response.json() == tweets
