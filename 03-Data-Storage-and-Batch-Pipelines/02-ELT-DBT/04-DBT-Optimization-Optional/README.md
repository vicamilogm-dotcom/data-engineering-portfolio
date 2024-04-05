## High level goal

There are 3 main issues in the previous setups we've done, that are not optimal
1. When picking data from the last 1000 days of the Hackernews dataset, we've harcoded in the code the value `1000` : this should never be the case. This variable should be centralized somewhere
2. When we were counting the `num_comments`, `num_stories`, the first and the last time those comments or stories were written : we were writing a lot of duplicated code.
3. If we were to document the project more, we would be defining the same fields multiple times, in different places. We should centralize this documentation.

❓ **_First : copy `dbt_lewagon` from the previous challenge section into this one_**

## 1️⃣ Create variables

- In the `dbt_project.yml`, introduce a variable called `last_x_days_history`, that you'll set to `1000`. And use that variable when building the `stg_hackernews_full.sql` model. Search the DBT documentation yourself to understand how things should be setup. Correction is in the `stg_hackernews_full.sql` and `dbt_project.yml` files
- Make sure 2 of the tests are green by runnin :
  - `make test_dbt_project_created`, and
  - `make test_dbt_variable_created`


## 2️⃣ Don't Repeat Yourself - Macros

- In the `mart_user` model, we were reusing some code a lot. In order to avoid that, write 3 macros (those macros should be written in a file you would create here : `dbt_lewagon/macros/models/mart_user.sql`) :
  - 1 called `num_types` : which takes a given type as an argument. Counts the distinct number of occurences of that type in the aggregation. And also returns the name of the column associated to this calculation.
  - 1 called `first_type_at` : which takes a given type as an argument. And returns when that type happened the first time (based on `created_at_local`) for a given level of aggregation. It also returns the name of the column associated to this calculation
  - 1 called `last_type_at` : same as above, but for the most recent occurence of the type
- To be more precise :
  - `{{ num_types('comment') }}` should output a piece of code like that : `COUNT(xxxxx) AS num_comment` (let's simplify and keep column names singular - this will change a bit from the previous name you gave to that column)
  - `{{ first_type_at('comment') }}` should output a piece of code like that : `OPERATION(xxxxx) AS first_comment_at` etc
  - If you need help on this, you can read this documentation : [Jinja](https://docs.getdbt.com/docs/building-a-dbt-project/jinja-macros)
- Run `make test` : 2 tests should be failing (they are related to the next exercice)

The correction is in 2 files :
- `mart_user_macro_1.sql` is the expected macro
- `mart_user_model_1.sql` is the `mart_user` model, modified to use the macro defined above

Your previous `mart_user` model should be calling macros 6 times total (3 macros per type. On 2 types).

- Build a macro called `key_metrics_per_type` which, for a given type `xxx`, builds the 3 key metrics :
  - `num_xxx`
  - `first_xxx_at`
  - `last_xxx_at`. Modify your `mart_user.sql` model to use this macro. It should now be calling it 2 times. 1 for each type.
- The correction is in 2 files :
  - `mart_user_macro_2.sql` is the expected macro
  - `mart_user_model_2.sql` is the expected `mart_user` model, modified to use the macro defined above.
- Run `make test` : all your tests should now be green.
- Push to git.
- As a next step, you could make the code even more succinct by writing a FOR loop that iterates over a list that gathers the different types - but there's very little value in this : for the sake of optimization, we would be sacrificing the readibility of the query.

## 3️⃣ Scaling your documentation and testing

- In the previous section, you're calling your macros with inputs that are hardcoded : type is `'comment'`, or `'story'`. This no longer works if the original type is changed by the HackerNews software engineers. Let's say they rename `'story'` and now call them `'post'`. `num_story` would be 0 for all new "posts" being written by the authors. Write a test which controls the distinct list of values for the `type` field.
  - In which `yml` file should you write this test ?
- The only model you've documented so far was the `mart_user` model. Quickly document the `stg_hackernews_comment`, `stg_hackernews_story`, and `stg_hackernews_full`. There are some fields that are repeated across all those models : instead of copy pasting the definitions, centralize their definitions in a `/models/central_documentation.md` file. To use this centralized documentation, leverage the `doc` jinja function.
- Implement a standard test which ensures referential integrity between the `user_id` in `mart_user` and the `author` in `stg_hackernews_full`
- The customer support team would like to spot potential bots, and have asked you to implement a test on the pipeline, which fails if, on a given day, a user has posted strictly more than 50 stories. How would you implement this ?
  - Note that this is not a "critical" test. Hence DBT should not throw an error if it fails, but rather send a "warning".

There is no correction for that last section. Ping the teacher if you need guidance.
