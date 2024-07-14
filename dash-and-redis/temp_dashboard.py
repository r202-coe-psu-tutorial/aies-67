from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px

import pandas
import redis
import plotly.express as px

app = Dash(__name__)

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

app.layout = html.Div(
    html.Div(
        [
            html.H4("Temp Live Feed"),
            dcc.Graph(id="live-update-graph"),
            dcc.Interval(
                id="interval-temp", interval=1 * 1000, n_intervals=0  # in milliseconds
            ),
        ]
    )
)


@callback(Output("live-update-graph", "figure"), Input("interval-temp", "n_intervals"))
def update_graph_live(n):

    data = redis_client.hgetall("temp")
    records = dict(date=data.keys(), temp=data.values())
    df = pandas.DataFrame.from_dict(records)
    df["temp"] = df["temp"].astype(float)
    fig = px.line(df, x="date", y="temp", title="Temperature")
    return fig


if __name__ == "__main__":
    app.run(debug=True)
