import mysql.connector
from  db_config import create_connection
# Récupérer les données climatiques depuis la base de données
connection = create_connection()
def fetch_weather_data(country):
    query = f"""
        SELECT t.Année AS Year, t.Mois, mm.precipitation, mm.temperature_max
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