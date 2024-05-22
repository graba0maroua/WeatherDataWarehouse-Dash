import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from FetchData import fetch_stations
from db_config import create_connection

# Define mapping for season names in French
seasons_mapping = {
    'Winter': 'Hiver',
    'Spring': 'Printemps',
    'Summer': 'Été',
    'Autumn': 'Automne'
}

# Define custom color palette for each season
season_colors = {
    'Winter': '#6495ED',  # Cornflower Blue
    'Spring': '#3CB371',  # Medium Sea Green
    'Summer': '#FF6347',  # Tomato
    'Autumn': '#FFA500'   # Orange
}

def fetch_temperature_data_at_station(city, selected_country):
    try:
        cnx = create_connection()
        cursor = cnx.cursor(dictionary=True)
        
        query = """
        SELECT t.Année, t.Saison,
            ROUND(AVG(m.temperature_max), 1) AS avg_temperature_max,
            ROUND(AVG(m.temperature_min), 1) AS avg_temperature_min,
            ROUND((AVG(m.temperature_max) + AVG(m.temperature_min)) / 2, 1) AS avg_temperature_avg
        FROM temps t
        JOIN mesures_météorologiques m ON t.id_date = m.id_date
        JOIN station s ON m.id_station = s.id_station
        WHERE s.Ville = %s AND s.Pays = %s
        GROUP BY t.Année, t.Saison
        """
        cursor.execute(query, (city, selected_country))
        data = cursor.fetchall()
        
        cursor.close()
        cnx.close()
        
        return data
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

stations = fetch_stations()
station_options = [{'label': station['ville'], 'value': station['ville']} for station in stations]

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div(style={
    'backgroundColor': '#f4f4f4',
    'padding': '30px',
    'fontFamily': 'Arial, sans-serif'
}, children=[
    html.H1("Évolution de la Température de par Saison", style={
        'color': '#333333',
        'textAlign': 'center',
        'fontSize': '2rem',
        'fontFamily': 'Open sans, sans-serif'
    }),
    html.P("Ce graphique montre l'évolution de la température  pour une station météorologique au fil des saisons de l'année",style={'color': '#333333', 'textAlign': 'center','fontSize':'1.2rem'}),

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
                style={'fontFamily': 'Lato, sans-serif', 'color': '#333'}
            ),
        ], style={'display': 'inline-block', 'width': '45%', 'paddingRight': '20px'}),
        html.Div([
            dcc.Dropdown(
                id='station-dropdown',
                options=station_options,
                value=stations[0]['ville'],
                clearable=False,
                placeholder="Sélectionnez une ville",
                style={'fontFamily': 'Lato, sans-serif', 'color': '#333'}
            ),
        ], style={'display': 'inline-block', 'width': '45%'}),
    ], style={'marginBottom': '40px'}),
    dcc.Loading(
        id="loading",
        type="default",
        children=html.Div(id='graph-container')
    ),
])

@app.callback(
    Output('graph-container', 'children'),
    [Input('station-dropdown', 'value'),
     Input('country-dropdown', 'value')]
)
def update_temperature_graph(city, selected_country):
    try:
        data = fetch_temperature_data_at_station(city, selected_country)
        df = pd.DataFrame(data)
        df['Saison'] = df['Saison'].map(seasons_mapping)
        
        fig_max = px.bar(df, x='Année', y='avg_temperature_max', color='Saison', 
                         title=f'Température Maximale Moyenne par Saison à {city} ({selected_country})',
                         color_discrete_map=season_colors)
        fig_max.update_layout(
            xaxis_title='Année (1920 - 2022)',
            yaxis_title='Température Maximale Moyenne (°C)',
            plot_bgcolor='white'
        )
        
        fig_min = px.bar(df, x='Année', y='avg_temperature_min', color='Saison', 
                         title=f'Température Minimale Moyenne par Saison à {city} ({selected_country})',
                         color_discrete_map=season_colors)
        fig_min.update_layout(
            xaxis_title='Année (1920 - 2022)',
            yaxis_title='Température Minimale Moyenne (°C)',
            plot_bgcolor='white'
        )
        
        fig_avg = px.bar(df, x='Année', y='avg_temperature_avg', color='Saison', 
                         title=f'Température Moyenne par Saison à {city} ({selected_country})',
                         color_discrete_map=season_colors)
        fig_avg.update_layout(
            xaxis_title='Année (1920 - 2022)',
            yaxis_title='Température Moyenne (°C)',
            plot_bgcolor='white'
        )
        
        graph_style = {
            'backgroundColor': '#fff',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
            'borderRadius': '10px',
            'padding': '20px',
            'marginBottom': '20px'
        }
        
        return html.Div([
            html.Div(dcc.Graph(figure=fig_max), style=graph_style),
            html.Div(dcc.Graph(figure=fig_min), style=graph_style),
            html.Div(dcc.Graph(figure=fig_avg), style=graph_style)
        ])
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return html.Div("An error occurred while fetching data.", style={'color': 'red', 'textAlign': 'center'})

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=False, dev_tools_props_check=False)
