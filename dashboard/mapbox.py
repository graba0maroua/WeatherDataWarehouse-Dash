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
        #     host=".......",
        #     database="...........",
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

def update_weather_map(selected_country, start_date, end_date):
    if selected_country is None or start_date is None or end_date is None:
        return pd.DataFrame()  # Return an empty DataFrame

    if conn is None:
        print("MySQL connection is not available.")
        return pd.DataFrame()  # Return an empty DataFrame

    # Execute SQL query to fetch data from the database
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT station.Ville, station.Latitude, station.Longitude, temps.Date, Mesures_Météorologiques.temperature_max,
               Mesures_Météorologiques.temperature_min, Mesures_Météorologiques.precipitation  
        FROM Mesures_Météorologiques             
        JOIN station ON Mesures_Météorologiques.id_station = station.id_station         
        JOIN temps ON Mesures_Météorologiques.id_date = temps.id_date            
        WHERE station.Pays = %s AND temps.Date BETWEEN %s AND %s            
        
    """, (selected_country, start_date, end_date))

    rows = cursor.fetchall()

    return pd.DataFrame(rows)  # Convert the fetched data into a DataFrame

# Define Dash app layout
app.layout = html.Div([
    dcc.Dropdown(
        id='country-dropdown',
        options=[
            {'label': 'Algeria', 'value': 'AG'},
            {'label': 'Morocco', 'value': 'MO'},
            {'label': 'TUNIS', 'value': 'TS'},
            
        ],
        value='MO'  
    ),
    dcc.DatePickerRange(
        id='date-range',
        min_date_allowed=pd.to_datetime('1920-01-01'),  # Adjust minimum date
        max_date_allowed=pd.to_datetime('today'),  # Allow up to today's date
        initial_visible_month=pd.to_datetime('2020-01-01'),  # Set initial view
        start_date=pd.to_datetime('2020-01-01').strftime('%Y-%m-%d'),  # Default start date
        end_date=pd.to_datetime('2020-01-10').strftime('%Y-%m-%d')  # Default end date
    ),
    dcc.Graph(id='weather-map'),
    html.Div(id='weather-data')
])


# Define callback to update the map
@app.callback(
    Output('weather-map', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_map(selected_country, start_date, end_date):
    
    weather_data = update_weather_map(selected_country, start_date, end_date)

    if weather_data.empty:
        return {}


    
  # Calculate minimum and maximum temperatures
    min_temp = weather_data['temperature_min'].min()
    max_temp = weather_data['temperature_min'].max()

  # Create a scatter map plot using plotly.express
    fig = px.scatter_mapbox(weather_data, lat="Latitude", lon="Longitude",
                          hover_name="Date",
                          hover_data={"Latitude": False, "Longitude": False, "Ville": True,
                                      "temperature_max": True, "temperature_min": True, "precipitation": True},
                          zoom=3, height=600)

    fig.update_layout(title=f"Weather in {selected_country} ({start_date} - {end_date})<br>Min Temp: {min_temp:.2f}°C, Max Temp: {max_temp:.2f}°C")

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)


