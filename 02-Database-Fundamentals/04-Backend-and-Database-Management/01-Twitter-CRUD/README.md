# 🎯 Goal

The goal of this exercise is to create:
- a Twitter **database** using *alembic*, containing a `tweets` and a `users` table
- and a functioning **back-end** integration with `FastAPI`

<br>

# 0️⃣ Setup: Creating the database with psql

❓ Lets create a new database in our postgres called `twitter`

<details>
<summary markdown='span'>Quickly make a database</summary>

```bash
createdb twitter
```

</details>

<br>

Our API will need a way to connect to postgres. We can do this with a [database URI](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING). You can think of this as the address to a specific database. We'll be using a `.env` to store our database address, as well as your postgres password (make sure to use the same password as last unit!)

Start by copying or renaming the `.env.sample` to `.env`, allow the `.env` to be readable by `direnv`, and make sure to update the contents:

```bash
POSTGRES_PASSWORD=mypassword # replace with the same password you used in the previous unit
POSTGRES_DATABASE_URL=postgresql+psycopg2://$USER:$POSTGRES_PASSWORD@localhost:5432/twitter
```

🔎 You might notice the additional `+psycopg2` at the beginning of our string, something we did not have in the previous unit. Here we are just defining the package that `sqlalchemy` should use to connect to the database.

Then, connect to our new database through DBeaver like we did in previous units!

Now we are ready to start creating our python files! 🚀

<br>

# 1️⃣ Python connection with sqlalchemy

We have set up a file for you at `twitter_api/database.py`. It has everything required to connect to the database from our API. Try to read it and understand how the code is working.

1. First we define the necessary imports from sqlalchemy.
    ```python
    import os
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
    ```

2. Next, we get our database URL string from the environment variable in our `.env`:
    ```python
    DB_URL = os.environ.get("POSTGRES_DATABASE_URL")
    ```

3. Now, we create an [engine](https://docs.sqlalchemy.org/en/20/core/engines.html), which is the point at which we are most abstracted away from the database. For us, it is the initial point of connection.
    ```python
    engine = create_engine(DB_URL)
    ```

    ```python
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    ```

4. You can now test your connection! Run the file `python twitter_api/database.py`, if it runs successfully, your postgres connection string and `sqlalchemy` is allowing us to execute queries against the database!
    ```python
    if __name__ == "__main__":
        query = text("""
            SELECT * FROM information_schema.tables
            WHERE table_schema = 'public'
            """
        )

        with SessionLocal() as db:
            print(db.execute(query).fetchall())
    ```

<br>

# 2️⃣ Creating the users table with alembic

❓ **Go to `twitter_api/models.py` and fill up the
`Users` class** using sqlalchemy [declarative mapping](https://docs.sqlalchemy.org/en/14/orm/mapping_styles.html).

Your mapping should be the equivalent to the SQL:
```sql
CREATE TABLE users (
	id serial4 PRIMARY KEY,
	email varchar NOT NULL UNIQUE,
	hashed_password varchar NOT NULL
);
```

💡 Start with just the table name and columns section.

Now that the table is defined, we are ready to use [alembic](https://alembic.sqlalchemy.org/en/latest/autogenerate.html) to autogenerate migrations!

The initial setup of alembic is a little tricky, so we have included the steps here:

1. The first step is to initialise `alembic`:
    ```bash
    alembic init alembic
    ```
    This will create an `alembic` folder in the challenge root.

2. Edit the `alembic/env.py` file in alembic folder, so as to:
    - Update `target_metadata` from None to a value that tells alembic to monitor any changes in tables defined by the `twitter_api.models module`. This value tells alembic where to look when auto generating migrations. Have a look at [alembic docs](https://alembic.sqlalchemy.org/en/latest/autogenerate.html) for an appropriate object.
    - Tell alembic how to connect to your postgres database. You could update `alembic.ini` line 58, but that would expose your `POSTGRES_PASSWORD` and you want to keep it private. Instead we can load environment variables directly from your `.env` inside `alembic/env.py` to define your postgres url:
    ```python
    import os
    import pathlib
    from dotenv import load_dotenv
    env_path = pathlib.Path(__file__).resolve().parent.parent.joinpath(".env")
    load_dotenv(env_path)
    config.set_main_option("sqlalchemy.url", os.environ["POSTGRES_DATABASE_URL"])
    ```

3. Now, our alembic should be setup and ready to go, you can run your first revision! 🚀
    ```bash
    alembic revision --autogenerate -m "added users table"
    ```

    This will generate a new file in `alembic/versions`, describing the changes to apply to the database.

    Let's have a look inside:

    <img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D4/inital-migration.png" width=400>

    We can see all of the commands alembic is running to create our `users` table. We can edit this as much as we like. One thing that can be useful when you create a table is to have a couple of rows added to test on. So, let's edit our migration to add those rows!

    Let's edit it to add these rows:
    ```python
    # Just save to a variable to able to apply a function to it.
    users = op.create_table(...)
    # Then we want to bulk insert our rows after creation.
    op.bulk_insert(users,
    [
        {'email':'oliver.giles@lewagon.org','hashed_password':'notreally'},
        {'email':'bruno@lewagon.org','hashed_password':'notreallyeither'}
    ])
    ```

4. Our new upgrade should look like this. Downgrade does not need editing because deleting the table gets rid of the rows. However, **usually you need to mirror your changes there!**

    <img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D4/edited-migration.png" width=400>


    You can then apply this to your (still empty) database by running:
    ```bash
    alembic upgrade head # head means: your latest database migration status (similar to git HEAD)
    ```

    👉 Go check your database, you should see a `users` table created with all the columns and two roles!

    ❗️ Note that there are some restrictions to what autogenerate will detect. You can more about them [here](https://alembic.sqlalchemy.org/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect).

<br>

# 3️⃣ Creating an API with FastAPI + Pydantic

We have three steps to creating the API:

1. Defining the pydantic models in `schemas.py`
2. Defining the functions to interact with the database in `crud.py`
3. Defining the endpoints in `main.py`


## 3.1. Pydantic: Create data schemas in `schemas.py`

If you look at the [pydantic documentation](https://pydantic-docs.helpmanual.io/usage/models/), you can see that inside fields for pydantic model the types are defined with type hints (for example `id: int`) compared to how we defined the tables in Alembic (`id = Column(Integer,...)`). We saw the power they give us for our APIs in the lecture, so let's try and build some for our `users` API.

 - Alembic `User()` model describe the columns of the SQL `users` table in `models.py`
 - Pydantic `UserBase()`, `UserCreate()`, and `User()` models describe how we would like to send and receive data from the API when we try to fill the User classes in `schemas.py`. It will help validate data types, as well as generate a docstring automatically for our FastAPI documentation later on!

❓ **Update schemas.py related to Users**: For that, ask yourself which piece of data should be available:
- for every operation - and therefore should belong in the `UserBase` model
- only when you are creating a user - and therefore should be added in the `UserCreate` model
- only when you query a user from the database - and therefore should be in the `User` model

<details>
<summary markdown='span'>🎁 Solution for when you are stuck or done!</summary>

```python
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    # This line allows the equivalent of ORM Mode
    model_config = ConfigDict(from_attributes=True)
```
</details>

Here, the main piece you were probably missing was the `model_config` to allow us to leverage the models using [ORM patterns](https://www.altexsoft.com/blog/object-relational-mapping/)!

## 3.2. Interact with the database via `FastAPI` without writing SQL (`crud.py` + `main.py`)

🎯 We want to create the four CRUD User functions in `crud.py`, and their associated FastAPI routes in `main.py`

### 3.2.1. `GET/users/user_id`
👉 We have provided the `crud.read_user` function:
```python
return db.query(models.User).filter(models.User.id == user_id).first()
```

Thanks to `sqlalchemy` you can see how we can interact with the DB without writing a single line of SQL!

👉 Now, check out `main.py`. The scaffolding is ready for you to start filling the API! We gave you the `main.read_user` function
```python
@app.get("/users/{user_id}", response_model=schemas.User, tags=["users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    """get endpoint to read a given user"""
    db_user = crud.read_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
```

🔎 The strangest thing here is `db: Session = Depends(get_db)`.
- Whenever a new request arrives, FastAPI will take care of calling your dependencies `get_db` first. It's just a way to refactor a piece of code that is shared for all API end-points.
- `get_db` creates a sqlalchemy [session](https://docs.sqlalchemy.org/en/14/orm/session_basics.html) that will be active until the API call ends: as soon as `main.read_user` returns, the `finally` condition on line 27 is called and the session (and DB connection) is closed. What we are doing is making sure every single call to the API has its own session with the DB. This is important for when we have multiple users making calls to create new users at the same time!

<details>
<summary markdown='span'>💡 Equivalent syntax without FastAPI "Depends" magic</summary>

```python
@app.get("/users/{user_id}", response_model=schemas.User, tags=["users"])
def read_user(user_id: int):
    """get endpoint to read a given user"""
    with SessionLocal() as db:
        # "with xxx" clause always run xxx.close() when finished
        db_user = crud.read_user(db, user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
    return db_user
```

</details>


👉 Let's run the app first and check out where we are starting from:
```bash
uvicorn twitter_api.main:app --reload
```

- Make sure port 8000 is forwarded from your VM to your local computer and go to `localhost:8000` to see your app running!
- As we populated our DB with two users in an earlier migration, you can test it out with [http://localhost:8000/users/1](http://localhost:8000/users/1).
- Make sure to check the [localhost:8000/docs](localhost:8000/docs) endpoint for some lovely automatically generated documentation - this is made possible because of the Pydantic models we defined in `schema.py`. FastAPI & Pydantic are working hand-in-hand to automatically create nice documentation.

### 3.2.2. `GET/users` endpoint

❓ This time it's your turn to code your logic in `crud.read_users` and then `main.read_users`.

- Check [sqlalchemy query syntax docs](https://docs.sqlalchemy.org/en/14/orm/query.html)
- Test your code at [http://localhost:8000/users](http://localhost:8000/users)

### 3.2.3. `POST/users` endpoint

This one is slightly more complex because you cannot create two users that have the same email (remember your condition from `models.py`)

- First check if user already exist using `crud.read_user_by_email`
- If so, raise a `HTTPException`
- If not, call `crud.create_user` to create a python instance of User within the current alchemy [DB Session](https://docs.sqlalchemy.org/en/14/orm/session_basics.html), then add and commit it to the DB.

🧪 Test your code and actually create a user using the API docs endpoint!

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D4/try.png" width=400>

🧪 You can now run the `users` tests (feel free to look at the tests for a reference to test APIs!):

```bash
make test_users
```

If you have 3/3 passed tests: add, commit and push your code to github!

<br>

# 4️⃣ Tweets 🦜

Now we want to create our tweets table, but don't worry, most of the code you have already written has patterns/logic that can be repeated here!

## 4.1. Create the table

❓ Lets return to our `models.py` and fill the `Tweet` class.

This time the SQL equivalent you should be aiming for is:
```sql
CREATE TABLE tweets (
    id serial PRIMARY KEY,
    "text" varchar NOT NULL,
    owner_id int NOT NULL REFERENCES users(id)
);
```

Watch out for the foreign key when we create the column:
```python
owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
```

❓ Now, complete `models.py` "Relationships" sections in `User` and `Tweet` classes we have been left unfilled so far.
- We want to be able to access the `user.tweets`
- We want to be able to access the `tweet.owner`

💡 This is call a 1-N relationship. Have a read of the [Alchemy docs](https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html) to get the syntax right!

<details>
<summary markdown='span'>🎁 Solution</summary>

In `User`:
```python
tweets = relationship("Tweet", back_populates="owner") # allows query "user.tweets"
```
In `Tweet`:
```python
owner = relationship("User", back_populates="tweets") # allows query "tweet.owner"
```

</details>

❓ Migrate your database with Tweets!
```bash
alembic revision --autogenerate -m "added tweets table"
alembic upgrade head
```

## 4.2. Create the schemas

❓ Now create the schemas for tweets. `TweetCreate` needs the same fields as `TweetBase`, you can just use `pass` if you don't want to add new fields from the inherited schema. We keep them separate in case at some point you want a new field in `TweetCreate` only.

## 4.3. Implement the endpoints

❓ Work through the tweet sections of `main.py` and `crud.py` to complete the app! The logic should be similar to the users endpoints.
- Start with the `POST/users/{user_id}/tweets/` route, and create some tweets!
- Then code the `GET/users/{user_id}/tweets/,` route and check that the relationship works by using `user.tweets` syntax

🧪 You can now run the `tweets` tests:
```bash
make test_tweets
```

If all the tests pass: add, commit and push your code to github!

<br>

# 5️⃣ Likes (optional)

🎯 Our last goal for today is to integrate the likes feature.

We want a new table with the SQL equivalent of:

```sql
CREATE TABLE likes (
	id serial NOT NULL PRIMARY KEY,
	owner_id int NOT NULL REFERENCES users(id),
	tweet_id int NOT NULL REFERENCES tweets(id)
);

```
As well as adding a `like_count` to tweets:
```sql
ALTER TABLE tweets
ADD COLUMN like_count INT DEFAULT 0
```

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/ER%20diagram%20tweets.png" width=400>

We want our ORM to enable two new **1-N relationship**:
- `user.likes` <--> `like.owner`
- `tweet.likes` <--> `like.tweet`

❓ **Create a `Like` model and update all the routes in `main.py`**

Notice the last route `GET/users/{user_id}/liked_tweets/` in particular!
- Here, we want to read all `liked_tweets` from a user.
- This is a **many-to-many (N-N) relationship** between users and tweets:
    - A **user** has many *liked_tweets*
    - A **tweet** has many *likers*

🧪 Once you think you have everything working, run the all the tests:
```bash
make test
```

<br>

# 🏁 Finishing up

Congratulations! You're now able to build your own REST API with `fastapi`, `pydantic`, `sqlalchemy` and `alembic`! 🚀

🧪 Don't forget to run:

```bash
make test
```

And git add, commit, and push your code to github so you can track you progress on Kitt!

### Further Reading

#### Inspect tests

If you've completed all the challenges for this unit, have a look at the way we build our tests: using a FastAPI [TestClient](https://fastapi.tiangolo.com/tutorial/testing/) to spawn a new server at each test, as well as a temporary local `sqlite` database to mimic your postgres instance!

Can you tell why with each `make test_...` we had to run all the tests that came before?

<details>
<summary markdown='span'>🎁 Solution</summary>

Because the tests are dumping the local `sqlite` database on every test run.

Our API's are inherently dependent on each other. When we test **likes**, they need to have **tweets** and **users** associated with them, so we need to maintain state. The easy way to do that is to just run the previous tests that creates tests users, tweets, and likes.

</details>


#### FastAPI Backend Template

📚 Bookmark, save, and have a read through this well-thought [FastAPI-Backend-Template](https://github.com/Aeternalis-Ingenium/FastAPI-Backend-Template) made by one of our Alumni: [Nino Lindenberg](https://kitt.lewagon.com/alumni/Artificial-Ninoligence)

It contains:
- FastAPI
- PostgreSQL via asynchronous SQLAlchemy 2.0
- Alembic for async database migration
- Docker
- CI for backend application with GitHub Actions
- CI for Pre-Commit auto-update
- Pre-Commit hooks
- CodeCov test report monitoring

<br>
