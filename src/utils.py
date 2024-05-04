import os
import pandas as pd

#* Function that drops columns
def drop_columns(folder_path, columns_to_drop):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            # Check if the columns to drop exist in the DataFrame
            columns_exist = all(col in df.columns for col in columns_to_drop)
            if columns_exist:
                # Drop the specified columns
                df.drop(columns=columns_to_drop, inplace=True)
                # Save the modified DataFrame to the processed folder
                processed_folder_path = os.path.join('data', 'processed', 'Algeria')
                os.makedirs(processed_folder_path, exist_ok=True)
                processed_file_path = os.path.join(processed_folder_path, file_name)
                df.to_csv(processed_file_path, index=False)
                print(f"{', '.join(columns_to_drop)} columns dropped and file saved: {processed_file_path}")
            else:
                print(f"At least one of the specified columns ({', '.join(columns_to_drop)}) not found in file: {file_name}")
