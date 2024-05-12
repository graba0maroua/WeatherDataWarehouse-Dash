import dash
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from FetchData import fetch_weather_data

app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Visualisation des données climatiques"),
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
    dcc.Graph(id='weather-graph')
])

@app.callback(
    Output('weather-graph', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_weather_graph(country):
    try:
        data = fetch_weather_data(country)
        df = pd.DataFrame(data)
        fig = px.line(df, x='Mois', y='temperature_max', color='Year',
                        title=f'Évolution de la température maximale en {country}',
                        labels={'temperature_max': 'Température maximale (°C)', 'Mois': 'Mois', 'Year': 'Année'})
        fig.update_layout(xaxis=dict(type='category'))
        return fig
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {}

if __name__ == '__main__':
    app.run_server(debug=True)
