# 🎯 Goal

🎯 We now want to leverage the CSVs of book data we created in the **Pandas** challenge to create a simple dashboard using **plotly** and **dash**. It should end up looking something like this:

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D2/example-dash.png">

For this exercise the code laying out the page is already in `dashboard.py`. Feel free to play around and modify it to your liking.

You can run the dashboard with:

```bash
python dashboard.py
```

Then forward port 8050 from your VM to your local machine, VSCode may have already done it for you. Check it out on **localhost:8050** or **127.0.0.1:8050** in your web browser 🚀

<br>

# 1️⃣ Graphs

In order to populate the dashboard just replace the `fig1` - `fig4` variables with the appropriate graphs.

Here are the relevant documentation pages for the different graphs:

- [bar chart](https://plotly.com/python/bar-charts/)
- [pie chart](https://plotly.com/python/pie-charts/)
- [line chart](https://plotly.com/python/line-charts/)

But feel free to experiment with any type of graph you want! 🚀

<br>

# 🏁 Finishing up

**Plotly** and **dash** are useful tools in order to build interactive dashboards and graphs. They are easy to use and integrate well with pandas and other python tools. At scale they are not as efficient as dedicated BI tools like Looker Studio or Tableau, but they are great for small projects!

Creating the logic in the previous exercise to output the CSV files has made the dashboard more responsive because we do not require pandas to do any computation in background before displaying the graphs!

<br>
