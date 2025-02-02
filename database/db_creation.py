import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import os

def create_connection():
    return mysql.connector.connect(
       host="localhost",
       user="...........",
       password="................",
    )
#Céation de la base de données 
def create_database(connection, database_name):
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE {database_name}")
        print(f"La Base de données {database_name} crée avec succès.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DB_CREATE_EXISTS:
            print(f"La Base de données {database_name} existe déjà.")
        else:
            print(f"Échec de création de la base de données : {err}")
    finally:
        cursor.close()
#Etablire une connection à la base de données 
def connect_to_database(database_name):
    return mysql.connector.connect(
        host="localhost",
        user="...............",
        password="................",
        database=database_name
    )
#Création des tables en respectant le shémas en étoile 
def create_tables(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS temps (
            id_date INT AUTO_INCREMENT PRIMARY KEY,
            Date DATETIME,
            Mois INT,
            Année INT,
            Saison VARCHAR(50),
            Trimestre INT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS station (
            id_station INT AUTO_INCREMENT PRIMARY KEY,
            Code_de_la_station VARCHAR(50),
            Nom_de_la_station VARCHAR(100),
            Pays VARCHAR(50),
            Ville VARCHAR(100),
            Latitude FLOAT,
            Longitude FLOAT,
            Elevation FLOAT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Mesures_Météorologiques (
            id_meteo INT AUTO_INCREMENT PRIMARY KEY,
            id_date INT,
            id_station INT,
            precipitation FLOAT,
            temperature_max FLOAT,
            temperature_min FLOAT,
            FOREIGN KEY (id_date) REFERENCES temps(id_date),
            FOREIGN KEY (id_station) REFERENCES station(id_station)
        )
    """)
    connection.commit()

def calculate_season(date):
    month = date.month
    if 3 <= month <= 5:
        return 'Spring'
    elif 6 <= month <= 8:
        return 'Summer'
    elif 9 <= month <= 11:
        return 'Autumn'
    else:
        return 'Winter'

def calculate_trimestre(date):
    month = date.month
    if month <= 3:
        return 1
    elif 4 <= month <= 6:
        return 2
    elif 7 <= month <= 9:
        return 3
    else:
        return 4

def extract_ville_pays(name):
    ville, pays = name.split(',')[0].strip(), name.split(',')[1].strip()
    return ville, pays
#Insertion des données données traitées dans les tables 
def insert_data(connection, file_path):
    df = pd.read_csv(file_path, parse_dates=['DATE'])
    cursor = connection.cursor()
    temp_ids = {}
    for index, row in df.iterrows():
        cursor.execute("""
            INSERT INTO temps (Date, Mois, Année, Saison, Trimestre)
            VALUES (%s, %s, %s, %s, %s)
        """, (row['DATE'], row['DATE'].month, row['DATE'].year, calculate_season(row['DATE']), calculate_trimestre(row['DATE'])))
        temp_id = cursor.lastrowid
        temp_ids[index] = temp_id

    station_ids = {}
    for index, row in df.iterrows():
        ville, pays = extract_ville_pays(row['NAME'])
        cursor.execute("""
            INSERT INTO station (Code_de_la_station, Nom_de_la_station, Pays, Ville, Latitude, Longitude, Elevation)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (row['STATION'], row['NAME'], pays, ville, row['LATITUDE'], row['LONGITUDE'], row['ELEVATION']))
        station_id = cursor.lastrowid
        station_ids[index] = station_id

    for index, row in df.iterrows():
        cursor.execute("""
            INSERT INTO Mesures_Météorologiques (id_date, id_station, precipitation, temperature_max, temperature_min)
            VALUES (%s, %s, %s, %s, %s)
        """, (temp_ids[index], station_ids[index], row['PRCP'], row['TMAX'], row['TMIN']))
    connection.commit()

def main():
    processed_folder = 'data/processed'
    connection = create_connection()
    create_database(connection, 'weather_datawarehouse')
    connection.close()
    
    connection = connect_to_database('weather_datawarehouse')
    create_tables(connection)

    for country_folder in os.listdir(processed_folder):
        country_folder_path = os.path.join(processed_folder, country_folder)
        
        if os.path.isdir(country_folder_path):
            for file_name in os.listdir(country_folder_path):
                if file_name.endswith('.csv'):
                    file_path = os.path.join(country_folder_path, file_name)
                    insert_data(connection, file_path)
    
    connection.close()
    print("Data insertion completed.")

if __name__ == "__main__":
    main()
