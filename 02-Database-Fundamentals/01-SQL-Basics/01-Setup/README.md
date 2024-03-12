# Setup

Let's prepare our database for the challenges of the day and then do a few warmup queries!

## Postgres in docker

We will create a volume to keep the data for today

```bash
docker volume create pgdata-0201
```

Launch the database, then connect via dbeaver (don't forget you need to port forward again vm -> host)

Setup your `.env`

```bash
cp .env.sample .env
```

Edit the environment variables, then run:

```bash
direnv reload
```

Launch the database!

```bash
docker run -p 5410:5432 -e POSTGRES_USER=$POSTGRES_USER -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD -v pgdata-0201:/var/lib/postgresql/data postgres:15.4
```

Create a database for the data for today [pagila](https://github.com/devrimgunduz/pagila)

```sql
CREATE DATABASE pagila;
```

Then, execute the following two commands back in the terminal to get the data into the database

```bash
curl -L https://raw.githubusercontent.com/devrimgunduz/pagila/e1e5a855c46176bc0e17b7e8dea2f61e555fb378/pagila-schema.sql | docker exec -i <your_container> psql --username=$POSTGRES_USER --dbname=pagila -a -f-
```

```bash
curl -L https://raw.githubusercontent.com/devrimgunduz/pagila/e1e5a855c46176bc0e17b7e8dea2f61e555fb378/pagila-data.sql | docker exec -i <your_container> psql --username=$POSTGRES_USER --dbname=pagila -a -f-
```

You are now ready to begin using the database!


## Actors


❓ Generate a list of actors who have acted in more than five films.

- Your output should have two columns: the `actor_id` and the `total_films` in which they have appeared. - Order the result by the number of films in descending order.
- Only include actors who have acted in more than five films in your result.

Once you are happy put your query into `actor_query.sql` and run

```
make test
```

## Rentals

❓ Produce a query that lists each film, its category, and the number of times it's been rented.

- Your output should have three columns: `title` (of the film), `category_name` (name of the category), and `rental_count` (number of times the film has been rented).
- Make sure to include films that have never been rented.
- Arrange the results by the `rental_count` in descending order, so that the most rented film appears first.

Once you are happy with your query, paste it into `rentals_query.sql` and run

```
make test
```

## Monthly revenue

❓ Calculate the monthly revenue for the year 2022

- Your output should consist of two columns: `month` (represented as a number from 1 to 12) and `monthly_revenue` (sum of all payment amounts for that month).
- Order the result by month in ascending order.

Once you are happy put your query into `monthly_revenue_query.sql` and run

```
make test
```

## Finish 🏁

Now that we have warmed up with a few queries, you are ready to move on and continue to work with this database and deal with some more advanced SQL.
