import dash
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from FetchData import fetch_precipitation_data

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Evolution of Precipitation by Country"),
    dcc.Dropdown(
        id='country-dropdown',
        options=[
            {'label': 'Algeria', 'value': 'AG'},
            {'label': 'Morocco', 'value': 'MO'},
            {'label': 'Tunisia', 'value': 'TS'}
        ],
        value='AG',
        clearable=False
    ),
    dcc.Graph(id='precipitation-graph')
])

@app.callback(
    Output('precipitation-graph', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_precipitation_graph(country):
    try:
        data = fetch_precipitation_data(country)
        df = pd.DataFrame(data)
        fig = px.line(df, x='Année', y='precipitation',
                title=f'Evolution of Precipitation in {country}',
                labels={'precipitation': 'Precipitation ', 'Année': 'Année'})
        return fig
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

if __name__ == '__main__':
    app.run_server(debug=True)