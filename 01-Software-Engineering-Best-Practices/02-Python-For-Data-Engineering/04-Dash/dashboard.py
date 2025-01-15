import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pathlib

DATA_PATH = pathlib.Path(__file__).resolve().parent.parent / "02-Pandas" / "data"

category_df = pd.read_csv(DATA_PATH / "category_distribution.csv")
best_books_df = pd.read_csv(DATA_PATH / "best_performing_books.csv")
author_df = pd.read_csv(DATA_PATH / "author_impact_analysis.csv")
review_years_df = pd.read_csv(DATA_PATH / "review_scores_over_time.csv")

fig1 = go.Figure()
pass  # YOUR CODE HERE

fig2 = go.Figure()
pass  # YOUR CODE HERE

fig3 = go.Figure()
pass  # YOUR CODE HERE

fig4 = go.Figure()
pass  # YOUR CODE HERE

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        html.H1("Book Data Analysis!", className="text-center my-4"),
        dbc.Row(dbc.Col(dcc.Graph(figure=fig1), width=12), className="my-2"),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=fig2), width=6),
                dbc.Col(dcc.Graph(figure=fig3), width=6),
            ],
            className="my-2",
        ),
        dbc.Row(dbc.Col(dcc.Graph(figure=fig4), width=12), className="my-2"),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
