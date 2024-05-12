from db_config import create_connection

# Récupérer les données climatiques depuis la base de données
connection = create_connection()

# Fetch precipitation data for a specific country
def fetch_precipitation_data(country):
    query = f"""
        SELECT t.Année , t.Mois, mm.precipitation
        FROM mesures_météorologiques mm
        INNER JOIN temps t ON mm.id_date = t.id_date
        INNER JOIN station s ON mm.id_station = s.id_station
        WHERE s.Pays = '{country}'
    """
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return data

def fetch_precipitation_data_at_station(city, selected_country):
    query = f"""
        SELECT t.Année , t.Mois, mm.precipitation
        FROM mesures_météorologiques mm
        INNER JOIN temps t ON mm.id_date = t.id_date
        INNER JOIN station s ON mm.id_station = s.id_station
        WHERE s.Ville = '{city}' 
            AND s.Pays = '{selected_country}'
    """
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return data

# Fetch stations data
def fetch_stations():
    query = """
        SELECT DISTINCT ville
        FROM station
    """
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    stations = cursor.fetchall()
    cursor.close()
    return stations
