import dash
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from FetchData import fetch_precipitation_data_at_station, fetch_stations

app = dash.Dash(__name__)

# Fetch station data for dropdown
stations = fetch_stations()  
station_options = [{'label': station['ville'], 'value': station['ville']} for station in stations]

# Define the layout of the app
app.layout = html.Div([
    html.H1("Evolution of Precipitation by Station"),
    dcc.Dropdown(
        id='station-dropdown',
        options=station_options,
        value=stations[0]['ville'],  # Default value to the first station
        clearable=False,
        placeholder="Select a City"
    ),
    dcc.Dropdown(
        id='country-dropdown',
        options=[
            {'label': 'Algeria', 'value': 'AG'},
            {'label': 'Morocco', 'value': 'MO'},
            {'label': 'Tunisia', 'value': 'TS'}
        ],
        value='AG',
        clearable=False,
        placeholder="Select a Country"
    ),
    dcc.Graph(id='precipitation-graph')
])

# Define the callback to update the graph based on user inputs
@app.callback(
    Output('precipitation-graph', 'figure'),
    [Input('station-dropdown', 'value'),
    Input('country-dropdown', 'value')]
)
def update_precipitation_graph(city,selected_country):
    try:
        data = fetch_precipitation_data_at_station(city,selected_country)
        df = pd.DataFrame(data)
        
        # Create the line chart
        fig = px.line(df, x='Year', y='precipitation',color='Mois', markers=True, 
                      title=f'Evolution of Precipitation Over Years at {city} ( {selected_country})')
        fig.update_xaxes(title_text='Year')
        fig.update_yaxes(title_text='Precipitation (mm)')
        return fig
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {}

if __name__ == '__main__':
    app.run_server(debug=True)
