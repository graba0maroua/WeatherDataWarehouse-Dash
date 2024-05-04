import os
import pandas as pd

# Définir le chemin du dossier 'Algeria'
dossier_algeria = 'Algeria'

def remove_columns_in_files(folder_path, columns_to_remove):
    """
    Remove specified columns from all CSV files in the specified folder.

    Parameters:
    - folder_path (str): Path to the folder containing the CSV files.
    - columns_to_remove (list): List of column names to be removed.
    """
    # Itérer à travers chaque fichier dans le dossier
    for nom_fichier in os.listdir(folder_path):
        if nom_fichier.endswith('.csv'):
            chemin_fichier = os.path.join(folder_path, nom_fichier)
            
            # Lire le fichier CSV dans un DataFrame
            df = pd.read_csv(chemin_fichier)
            
            # Supprimer les colonnes spécifiées
            df.drop(columns_to_remove, axis=1, inplace=True)
            
            # Enregistrer le DataFrame modifié dans le fichier CSV
            df.to_csv(chemin_fichier, index=False)

            print(f"Les colonnes {columns_to_remove} ont été supprimées de '{nom_fichier}'")


def convert_date_to_datetime(folder_path):
    """
    Convert the 'DATE' column to datetime format in all CSV files in the specified folder.
    Parameters:
    - folder_path (str): Path to the folder containing the CSV files.
    """
    # Itérer à travers chaque fichier dans le dossier
    for nom_fichier in os.listdir(folder_path):
        if nom_fichier.endswith('.csv'):
            chemin_fichier = os.path.join(folder_path, nom_fichier)
            
            # Lire le fichier CSV dans un DataFrame
            df = pd.read_csv(chemin_fichier)
            
            # Convertir la colonne 'DATE' en format datetime
            df['DATE'] = pd.to_datetime(df['DATE'])

            # Enregistrer le DataFrame modifié dans le fichier CSV
            df.to_csv(chemin_fichier, index=False)

            print(f"La colonne 'DATE' a été convertie en format datetime dans '{nom_fichier}'")

#* Appeler la fonction avec le chemin du dossier contenant les fichiers CSV
# convert_date_to_datetime('Algeria')

def fill_missing_TMIN_with_next_mean(df):
    # Create a copy of the DataFrame to avoid modifying the original
    df_copy = df.copy()
    # Fill missing values in TMIN column with the mean of the next 5 non-NaN values
    for index, row in df_copy.iterrows():
        if pd.isna(row['TMIN']):
            # Select the next 5 rows after the current index
            next_values = df_copy.loc[index+1:index+5, 'TMIN'].dropna()
            # Check if there are enough non-NaN values in the next 5 rows
            if len(next_values) > 0:
                # Calculate the mean of the next non-NaN values and fill the missing value
                df_copy.at[index, 'TMIN'] = next_values.mean()
            else:
                # If there are not enough non-NaN values in the next 5 rows, continue searching
                offset = 1
                while len(next_values) == 0 and index+offset < len(df_copy):
                    next_values = df_copy.loc[index+offset:index+offset+5, 'TMIN'].dropna()
                    offset += 1
                # If non-NaN values are found, calculate the mean and fill the missing value
                if len(next_values) > 0:
                    df_copy.at[index, 'TMIN'] = next_values.mean()
                # If there are still no non-NaN values, fill with NaN
                else:
                    df_copy.at[index, 'TMIN'] = None
    return df_copy

def fill_missing_TMIN():
# Définir le chemin du dossier Algeria
    folder_path = 'Algeria'
# Itérer à travers chaque fichier dans le dossier
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
        # Lire le fichier CSV dans un DataFrame
        df = pd.read_csv(file_path)
        
        # Appliquer la fonction fill_missing_TMIN_with_next_mean
        df = fill_missing_TMIN_with_next_mean(df)
        
        # Enregistrer le DataFrame modifié dans le même fichier CSV
        df.to_csv(file_path, index=False)
        
        print(f"Les valeurs manquantes dans TMIN ont été remplacées par la moyenne des 5 valeurs suivantes dans '{file_name}'")

import os
import pandas as pd

def fill_missing_TMIN_ATTRIBUTES(df):
    # Create a copy of the DataFrame to avoid modifying the original
    df_copy = df.copy()
    # Fill missing values in TMIN_ATTRIBUTES column with the most common value in the next 5 non-NaN values
    for index, row in df_copy.iterrows():
        if pd.isna(row['TMIN_ATTRIBUTES']):
            next_values = df_copy.loc[index+1:index+5, 'TMIN_ATTRIBUTES'].dropna()
            if len(next_values) > 0:
                most_common_value = next_values.mode()[0]
                df_copy.at[index, 'TMIN_ATTRIBUTES'] = most_common_value
            else:
                # If there are no non-NaN values in the next 5 rows or we reach the end of the DataFrame, stop searching
                if index + 5 >= len(df_copy):
                    break
                # Continue searching
                offset = 1
                while len(next_values) == 0:
                    if index + offset + 5 >= len(df_copy):
                        break
                    next_values = df_copy.loc[index+offset:index+offset+5, 'TMIN_ATTRIBUTES'].dropna()
                    offset += 1
                if len(next_values) > 0:
                    most_common_value = next_values.mode()[0]
                    df_copy.at[index, 'TMIN_ATTRIBUTES'] = most_common_value
    return df_copy


def process_TMIN_ATTRIBUTES_files(folder_path):
    # Itérer à travers chaque fichier dans le dossier
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            # Lire le fichier CSV dans un DataFrame
            df = pd.read_csv(file_path)
            # Appliquer la fonction fill_missing_TMIN_ATTRIBUTES à votre DataFrame
            df = fill_missing_TMIN_ATTRIBUTES(df)
            # Enregistrer le DataFrame modifié dans le même fichier CSV
            df.to_csv(file_path, index=False)
            print(f"Les valeurs manquantes dans TMIN_ATTRIBUTES ont été remplacées dans '{file_name}'")

# Utilisation de la fonction process_TMIN_ATTRIBUTES_files pour traiter tous les fichiers CSV dans le dossier Algeria
folder_path = 'Algeria'
process_TMIN_ATTRIBUTES_files(folder_path)

