import os
import pandas as pd

def check_csv_for_nan(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            nan_values = df.isnull().values.any()
            if nan_values:
                print(f"NaN values found in file: {file_path}")
            else:
                print(f"No NaN values found in file: {file_path}")

folders = ['data/processed/Algeria', 'data/processed/Morroco', 'data/processed/Tunisia']

for folder in folders:
    print(f"Checking folder: {folder}")
    check_csv_for_nan(folder)
