import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from FetchData import  fetch_stations
from database.db_config import create_connection

def fetch_temperature_data_at_station(city, selected_country):
    try:
        # Connect to your MySQL database
        cnx =create_connection()
        cursor = cnx.cursor(dictionary=True)
        
        # Execute SQL query to fetch temperature data for the specified station
        query = """
        SELECT t.Année,
            ROUND(AVG(m.temperature_max), 1) AS "température maximale",
            ROUND(AVG(m.temperature_min), 1) AS "température minimale",
            ROUND((AVG(m.temperature_max) + AVG(m.temperature_min)) / 2, 1) AS "température moyenne"
        FROM temps t
        JOIN mesures_météorologiques m ON t.id_date = m.id_date
        JOIN station s ON m.id_station = s.id_station
        WHERE s.Ville = %s AND s.Pays = %s
        GROUP BY t.Année
        """
        cursor.execute(query, (city, selected_country))
        
        # Fetch all rows of the result
        data = cursor.fetchall()
        
        # Close the cursor and database connection
        cursor.close()
        cnx.close()
        
        return data
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
# Fetch station data for dropdown
stations = fetch_stations()
station_options = [{'label': station['ville'], 'value': station['ville']} for station in stations]

# Define the layout of the app
app = dash.Dash(__name__)

app.layout = html.Div(style={'backgroundColor': '#f9f9f9', 'padding': '20px'}, children=[
    html.H1("Évolution de la température par pays", style={'color': '#333333', 'textAlign': 'center','fontFamily': 'Open Sans, sans-serif'}),
    html.P("Ce graphique montre l'évolution de la température au fil des ans pour une station météorologique donnée.",style={'color': '#333333', 'textAlign': 'center','fontSize':'1.4rem'}),
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
        ], style={'display': 'inline-block', 'width': '45%', 'margin': '10px'}),
        html.Div([
            dcc.Dropdown(
                id='station-dropdown',
                options=station_options,
                value=stations[0]['ville'],  # Default value to the first station
                clearable=False,
                placeholder="Select a City",
                style={'fontFamily': 'Lato'}
            ),
        ], style={'display': 'inline-block', 'width': '45%', 'margin': '10px'}),
    ]),
    html.Div(id='graph-container', style={'backgroundColor': 'white', 'boxShadow': '2px 2px 8px rgba(0, 0, 0, 0.1)', 'borderRadius': '10px'}),
])

# Define the callback to update the graph based on user inputs
@app.callback(
    Output('graph-container', 'children'),
    [Input('station-dropdown', 'value'),
     Input('country-dropdown', 'value')]
)
def update_temperature_graph(city, selected_country):
    try:
        data = fetch_temperature_data_at_station(city, selected_country)
        df = pd.DataFrame(data)
        
        # Create line chart for temperature metrics
        fig = px.line(df, x='Année', 
                      y=['température maximale', 'température minimale', 'température moyenne'], 
                      title=f'Évolution de la température  à {city} ({selected_country})')
        fig.update_xaxes(title_text='Année (1920 - 2022)', showgrid=False)
        fig.update_yaxes(title_text='Température (°C)', showgrid=False)
        
        return dcc.Graph(figure=fig)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return html.Div("An error occurred while fetching data.", style={'color': 'red'})

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=False, dev_tools_props_check=False)
