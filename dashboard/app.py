import dash
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from FetchData import fetch_precipitation_data_at_station, fetch_stations

app = dash.Dash(__name__)
months_mapping = {
    1: 'janvier', 2: 'février', 3: 'mars', 4: 'avril', 5: 'mai', 6: 'juin',
    7: 'juillet', 8: 'août', 9: 'septembre', 10: 'octobre', 11: 'novembre', 12: 'décembre'
}
# Fetch station data for dropdown
stations = fetch_stations()  
station_options = [{'label': station['ville'], 'value': station['ville']} for station in stations]

# Define the layout of the app
app.layout = html.Div([
    html.H1("Évolution de la précipitation par station", style={'color': '#333333', 'text-align': 'center'}),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='country-dropdown',
                options=[
                   {'label': 'Algérie', 'value': 'AG'},
                    {'label': 'Maroc', 'value': 'MO'},
                    {'label': 'Tunisie', 'value': 'TS'}
                ],
                value='AG',
                clearable=False,
                placeholder="Sélectionnez un pays",
                style={'fontFamily': 'Lato'}
            ),
        ], style={'display': 'inline-block', 'width': '45%', 'margin-left': '2%', 'margin-right': '2%'}),
        html.Div([
            dcc.Dropdown(
                id='station-dropdown',
                options=station_options,
                value=stations[0]['ville'],  # Default value to the first station
                clearable=False,
                placeholder="Select a City",
            ),
        ], style={'display': 'inline-block', 'width': '45%'}),
    ]),
    dcc.Graph(id='precipitation-graph')
])

# Define the callback to update the graph based on user inputs
@app.callback(
    Output('precipitation-graph', 'figure'),
    [Input('station-dropdown', 'value'),
    Input('country-dropdown', 'value')]
)
def update_precipitation_graph(city, selected_country):
    try:
        data = fetch_precipitation_data_at_station(city, selected_country)
        df = pd.DataFrame(data)
        # Replace numerical month values with French names
        df['Mois'] = df['Mois'].map(months_mapping)
        # Create the line chart
        fig = px.line(df, x='Année', y='precipitation', color='Mois', markers=True, 
                      title=f'Évolution de la précipitation au fil des ans à {city} ({selected_country})')
        fig.update_xaxes(title_text='Année (1920 - 2022)')
        fig.update_yaxes(title_text='Précipitation (PRCP)')
        return fig
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {}

if __name__ == '__main__':
    app.run_server(debug=True)
