# 🎯 Goal

The finance team have come back to us and want us to add the margin percent to their models. This could be a common calculation and a perfect place to use **macros**. Macros allow you to create functions that can be re-used in different models, keeping your models nice and [DRY](https://en.wikipedia.org/wiki/Don't_repeat_yourself).

Macros are similar to python functions, allowing you to do things like:
- Define common operations used across multiple models
- Import packages to use predefined functions created by other developers, like we did for tests in the previous challenge

In this challenge we will create a simple macro to calculate a percentage as an additional field that you could use across multiple models.

❓ **First: copy `dbt_lewagon` from the previous challenge section into this one**

<br>

# 1️⃣ Create a margin_percent macro

Like models in DBT, macros are defined in SQL and leverage Jinja templating.

- In the `macros/` directory, create a `functions.sql` file.
- Using [DBT's documentation at this link](https://docs.getdbt.com/docs/build/jinja-macros#macros) on Jinja macros, define the macro: `margin_percent` with the following parameters:
    - The macro should take the columns `revenue` and `purchase_cost` as inputs
    - Define what the macro should return: `margin_percent` = `margin` / `revenue`
    - Round the result to two decimal places, but provide an option for the user to control how many decimal places so show.

<details>
<summary markdown='span'>💡 Hints</summary>

Basic macro structure

```sql
{% macro macro_name(column_name1, column_name2, macro_var=2, ...) %}
    <your_macro_code_here>
{% endmacro %}
```

There is a built in SQL function, `SAFE_DIVIDE()`, to prevent an error when dividing by zero.

</details>

When you think you have a working macro, edit your `int_sales_margin.sql` model to add a column with `margin_percent`.

🧪 To test your model and macro, run:

```bash
make test
```

<br>

# 🏁 Finishing up

Congratulations, you've touched the surface of creating macros in your DBT project. This idea is extensible and works similar to python functions where you can have nested macros to perform more complex operations. For more information, check out DBT's documentation on Jinja and macros at [this link](https://docs.getdbt.com/docs/build/jinja-macros).

Make sure to run `make test` and git add, commit, and push your code to GitHub to track your progress on Kitt!

<br>
