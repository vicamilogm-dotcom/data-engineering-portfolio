# 🎯 Goals

You've created your first staging models, which are refined versions of the `source` data inherited from the BigQuery dataset. This section has 2 goals:
- Building on top of the `stg_hackernews_full` model by creating a mart model that could be useful to endusers.
- Making your pipeline healthier, by implementing some tests.
- Making the data you're surfacing to business stakeholders more readable, by documenting the meaning of your models.

❗ **First: copy `dbt_lewagon` from the previous challenge into this challenge** ❗

<br>

# 1️⃣ Enrich the mart layer

Our goal is to create a mart layer model that builds on the previous created `stg_hackernews_full` model.

- Under the `models/mart/` folder, create a file called `mart_user.sql`. It will log key information about the Hackernews users.
- Configure the model this way:
  - It should be a `view` materialization
  - It should be based on the `stg_hackernews_full` model
  - It should be composed of this list of fields (**Suggested approach: do not try to write SQL for all the fields at once. Start with one very simple config, outputting 1 or 2 fields. Then run your model and make sure the view is created in BigQuery, then iterate.**)
    - `user_id`
    - `num_comments`: the total number of comments made by the author
    - `first_comment_at`: when the user made his first comment on HackerNews
    - `last_comment_at`:  when the user made his last comment on HackerNews
    - `num_stories`:  the total number of stories made by the author
    - `first_story_at`:  when the user made his first story on HackerNews
    - `last_story_at`: when the user made his last story on HackerNews
- Run your model to make sure it works.

Now we want to be able to make sure that our way of calculating the `num_stories`, `num_comments` made by a user is correct. This is called **QA**. To do that, you will need, for a given `user_id`, to go check on the HackerNews' website if the volume of activites observed there matches the values in your `mart_user` model.

- To facilitate this, let's add a new field to the `mart_user` model: `user_url` which brings you to the welcome page of the user, where you can see the history of stories or comments they posted.
    <details>
    <summary markdown='span'>💡 Hint</summary>
    This URL looks something like this: `https://news.ycombinator.com/user?id=`
    </details>
- Surface this new field in BigQuery by running the model again.
- Run `make test_mart_user` to make sure the structure of your model is correct.
- **No code is needed in this section** - Now that you have this field handy, it should facilitate your QA: pick a few `user_id` in your BigQuery model, and verify that the `num_comments` or `num_stories` you calculated for this user matches the `num_comments` and `num_stories` you can count on the HackerNews website, that they wrote in the past 1000 days.

<br>

# 2️⃣ Document your models and add some tests

You've built a few models already - some stakeholders in your company may need to use your models, for dashboarding or machine learning workloads. You should document what each field means. DBT has a standard way of documenting models - and this documentation can then be parsed and viewed on a web page, accessible by everyone in the company.

- Under the  `models/mart/` folder, create a file called `models.yml`.
- Following the instructions on how to properly document a model: [Documentation](https://docs.getdbt.com/docs/building-a-dbt-project/documentation), document the `mart_user` model.
  - Provide a high level `description` of the model itself
  - Provide a high level `description` of all the columns
- Implement 3 tests: you should not write custom tests (meaning there shouldn't be any piece of SQL code written for those tests, and they should be implemented in the `models.yml` file directly)
  - 1 that checks that `user_id` is unique and always populated
  - 1 that checks that `num_comments` is always greater or equal to 0
  - 1 that checks that `num_stories` is always greater or equal to 0

    <details>
    <summary markdown='span'>💡 Hint</summary>
    For the "always greater or equal to 0", have a look around for a pre-build test. You will need to install a DBT package that enables you to very simply configure this type of test: [dbt_utils](https://hub.getdbt.com/dbt-labs/dbt_utils/0.8.6/). Install the 0.8.6 version. You'll need to create a `packages.yml` file at the same level as the `dbt_project.yml` file.
    </details>

- Run `make test` to test your code. If it passes, git add, commit, and push your code to github!

<br>

# 3️⃣ Run the tests

Let's make sure all the tests you've written are green: run `dbt test`

If tests are failing, check the compiled SQL file referenced in the error message - a great way to debug is to copy paste the SQL code and execute it in BigQuery what records are being returned, and why the test is failing.

<br>

# 4️⃣ Generating and viewing the documentation

You now have a robust DBT project: models that are dependent on each other. Documentation on the meaning of each field. Listing some tests etc. Let's expose this documentation so it's easily viewable.

You can find most of commands we'll run in these [docs](https://docs.getdbt.com/reference/commands/cmd-docs), with some additional context and detail.

## 4.1. Viewing your DBT Documentation

To generate and serve docs you can use the following commands:

```bash
# Generate the documentation
dbt docs generate
```

```bash
# Surface the documentation in a web GUI
dbt docs serve
```

The previous command open a page in your browser, have a look around! When you're ready, check the "Database" section to find the structure of your BigQuery project, the datasets in the project, the tables and views inside each dataset, as well as the documentation of each field. Especially, go to:

- Database > your project name > your dataset name > `mart_user` - you should see the documentation and tests for each field.

## 4.2. Lineage graph

Click on `stg_hackernews_full`, which you have not documented. At the bottom right of the screen click on the little blue logo, called `View Lineage Graph`. You can now see how your model is related to other models.

<br>

# 🏁 Finishing up

Congratulations! You've created a DBT model that sources data from BigQuery, stages, and creates a mart layer that is usable by an enduser! In the next challenge, we'll look at removing hardcoded values with more Jinja syntax.

To test your DBT project, run:

```bash
`make test`
```

Don't forget to git add, commit, and push your code to github so you can track your progress on Kitt!

<br>
