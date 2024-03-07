# Dashboards with Dash

🎯 We now want to leverage those csvs we created in the last exercise to create a simple dashboard using plotly and dash it should end up looking something like this:

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D2/example-dash.png">

For this exercise the code laying out the page is already in `dashboard.py` feel free to modify it as you see fit.

You can run the dashboard with:

```
python dashboard.py
```

then port forward and check it out on port 8050 🚀

# Graphs

In order to populate it just replace the fig1 - fig4 variables with the appropriate graphs.

Here are the relevant documentation pages for the different graphs:

-[bar chart](https://plotly.com/python/bar-charts/)
-[pie chart](https://plotly.com/python/pie-charts/)
-[line chart](https://plotly.com/python/line-charts/)

But feel free to experiment with any type of graph you want!

# Finish 🏁

Dash and plotly are very useful tools in order to build interactive dashboards and graphs. They are also very easy to use and integrate with pandas and other python tools. At scale they are not as efficent as dedicated BI tools like Tableau or Looker but they are a great way to work for small projects!

Creating the logic in the prior exercise to output the csvs has made the dashboard more responsive as we don't rely pandas computing in background before displaying the graphs!
