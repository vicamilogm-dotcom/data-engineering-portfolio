# 🎯 Goals

Postgres has some advanced features available, including vectorised text search.

The goal of this exercise will be to leverage the full text search capacity of Postgres to build a recommendation system for films.

Like the previous challenges, iterate towards your solution using DBeaver. To run the unit tests, copy and paste the query into the relevant SQL file in the challenge directory on your VM.

We will use the same database as the previous challenge, so copy across your `.env`.

```bash
cp ../01-Setup/.env .
```

<br>

# 1️⃣ Text Search with Ranking

#### Objective:

Find films in the Pagila database that are related to the word "Cat" based on their `description`. Also, rank the films by the relevance of the keywords in the `description`.

#### Instructions:

1. Use the `to_tsvector` function to convert the `description` column to a text-search vector.
2. Use the `@@` operator to perform the actual text search.
3. Utilize the `ts_rank` function to rank your results by relevance.
4. Sort your results by the rank in descending order.

🧪 Once you have a query, paste it into `text_search_query.sql` and run:

```bash
make test
```

<br>

# 2️⃣ Simple Recommendation Engine

#### Objective:

Given a film title 'APOCALYPSE FLAMINGOS', recommend other films with similar `description`s.

#### Instructions:

1. Create a CTE (Common Table Expression) that holds the text-search vector of the `description` of the given film.
2. Use the CTE to find similar films based on the `description` text-search vector.
3. Ensure that the film used in the CTE is not included in your final list of recommendations.

🧪 Once you have a query, paste it into `recommendation_query.sql` and run:

```bash
make test
```

<br>

# 3️⃣ Improved query ranking

#### Objective:

Improve the original query by using `ts_rank_cd` instead of `ts_rank` this time looking at 'Cat & Dog'

#### Instructions:

1. Use the `ts_rank_cd` function to rank your results by relevance.

🧪 Once you have a query, paste it into `improved_text_search_query.sql` and run:

```bash
make test
```

<br>

# 4️⃣ (Optional) Put it in a python script

Try to implement all the functions in the `recommendation.py` script by following the doc strings.

At the end you should have a command line tool that can recommend movies based on a users input!

<br>

# 🏁 Finish

We now have a cool way to recommend new movies! 🎉

<br>
