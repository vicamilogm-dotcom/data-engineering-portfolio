# ❗ Legacy Challenge ❗

This is a legacy challenge and has been archived as is.

It has been left available if you want to practice, but will not contribute towards your mandatory challenge completion percentage as part of the Le Wagon Data Engineering Bootcamp.

If you want to do these challenges, here are a few notes:
- The `pyproject.toml` has been renamed to `pyproject.toml.bak`.
    - This was done so that a virtual environment for this challenge was not installed when your ran `make install` on Setup Day, reducing disk usage.
    - If you want to install the poetry virtual environment, rename the `pyproject.toml.bak` to `pyproject.toml` and run: `poetry install`
    - You may need change the path of the package: `lewagonde` in the `pyproject.toml`. `lewagonde` contains helper functions for testing.
- Consider creating a new dbt profile for these challenges. Such as: `dbt_hackernews`

## Goals

There are several options during this recap
- Either go through the correction of the exercises
- Go through the optimisation of DBT processes
  - Setting up variables
  - Building macros
  - Building incremental models
- Showing what true `production` and `dev` environment look like in BigQuery
- Go through the BigQuery cost optimization + cost tracking in BigQuery itself
