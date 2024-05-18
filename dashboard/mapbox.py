import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import mysql.connector

# Initialize Dash app
app = dash.Dash(__name__)

def establish_database_connection():
    try:
        # conn = mysql.connector.connect(
        #     host="......",
        #     database="..........",
        #     user=".........",
        #     password="........"
        # )
        print(f"database connected")
        return conn
        
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

# Connect to the MySQL database
conn = establish_database_connection()

def update_weather_map(selected_countries, start_date, end_date):
    global conn  # Declare conn as global

    if not selected_countries or start_date is None or end_date is None:
        return pd.DataFrame()  # Return an empty DataFrame

    # Re-establish MySQL connection if it's closed or lost
    if conn is None or not conn.is_connected():
        conn = establish_database_connection()

    if conn is None:
        print("MySQL connection is not available.")
        return pd.DataFrame()  # Return an empty DataFrame

    # Construct the IN clause for multiple countries
    country_in_clause = ", ".join(["'%s'" % country for country in selected_countries])

    # Execute SQL query to fetch data from the database for multiple countries
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"""
    
    SELECT station.Ville, station.Latitude, station.Longitude,
        MAX(Mesures_Météorologiques.temperature_max) AS temperature_max,
        MIN(Mesures_Météorologiques.temperature_min) AS temperature_min,
        AVG(Mesures_Météorologiques.precipitation) AS precipitation
    FROM Mesures_Météorologiques
    JOIN station ON Mesures_Météorologiques.id_station = station.id_station
    JOIN temps ON Mesures_Météorologiques.id_date = temps.id_date
    WHERE station.Pays IN ({country_in_clause}) AND temps.Date BETWEEN %s AND %s
    GROUP BY station.Ville, station.Latitude, station.Longitude


""", (start_date, end_date))

    rows = cursor.fetchall()

    return pd.DataFrame(rows)  # Convert the fetched data into a DataFrame

# Define CSS styles for elements
external_stylesheets = {
    'background-color': '#f8f9fa',
    'padding': '20px'
}

# Apply styles to components
app.layout = html.Div(style=external_stylesheets, children=[
    html.H1('Weather Data Visualization', style={'text-align': 'center'}),
    html.Div([
        dcc.Dropdown(
            id='country-dropdown',
            options=[
                {'label': 'Algeria', 'value': 'AG'},
                {'label': 'Morocco', 'value': 'MO'},
                {'label': 'Tunisia', 'value': 'TS'},  
            ],
            value=['MO'],  # Set default value to MO
            multi=True,  # Allow multiple selections
            style={'width': '50%'}
        ),
        dcc.DatePickerRange(
            id='date-range',
            min_date_allowed=pd.to_datetime('1920-01-01'),
            max_date_allowed=pd.to_datetime('today'),
            initial_visible_month=pd.to_datetime('2020-01-01'),
            start_date=pd.to_datetime('2020-01-01').strftime('%Y-%m-%d'),
            end_date=pd.to_datetime('2020-01-10').strftime('%Y-%m-%d'),
            style={'margin-top': '10px'}
        ),
    ], style={'display': 'flex', 'justify-content': 'center'}),
    dcc.Loading(
        id="loading-weather-map",
        type="default",
        children=[
            dcc.Graph(id='weather-map')
        ]
    ),
    html.Div(id='weather-data', style={'margin-top': '20px', 'text-align': 'center'})
])

# Define callback to update the map

@app.callback(
    Output('weather-map', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_map(selected_countries, start_date, end_date):
    # Fetch weather data from the database
    print(f"Selected Countries: {selected_countries}")
    print(f"Start Date: {start_date}, End Date: {end_date}")
    weather_data = update_weather_map(selected_countries, start_date, end_date)

    # Check if weather data is empty
    if weather_data.empty:
        return {}

    # Create a scatter map plot using Plotly Express
    fig = px.scatter_mapbox(weather_data, lat="Latitude", lon="Longitude",
                            hover_name="Ville",
                            hover_data={"precipitation": True,
                                        "temperature_min": True,
                                        "temperature_max": True},
                            zoom=3, height=600,
                           )

    fig.update_layout(title=f"Weather in {' & '.join(selected_countries)} ({start_date} - {end_date})",
                      mapbox_style="open-street-map",
                      margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=False, dev_tools_props_check=False)
