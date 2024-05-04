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


def drop_TAVG_TAVG_ATTRIBUTES():
    folder_path = os.path.join('data', 'raw', 'Algeria')
# Define the columns to drop
    columns_to_drop = ['TAVG', 'TAVG_ATTRIBUTES']
# Call the function from utils.py to drop the specified columns from all CSV files in the folder
    drop_columns(folder_path, columns_to_drop)


#* Function that fills missing TMIN
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
                df_copy.at[index, 'TMIN'] = round(next_values.mean(), 1)
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



def fill_missing_TMIN_with_prev_mean(df):
    df_copy = df.copy()
    for index, row in df_copy.iterrows():
        if pd.isna(row['TMIN']):
            prev_values = df_copy.loc[max(0, index-5):index-1, 'TMIN'].dropna()
            if len(prev_values) > 0:
                df_copy.at[index, 'TMIN'] = round(prev_values.mean(), 1)  # Round to 1 decimal place
            else:
                offset = 1
                while len(prev_values) == 0 and index+offset < len(df_copy):
                    prev_values = df_copy.loc[max(0, index-offset-5):index-offset-1, 'TMIN'].dropna()
                    offset += 1
                if len(prev_values) > 0:
                    df_copy.at[index, 'TMIN'] = round(prev_values.mean(), 1)  # Round to 1 decimal place
                else:
                    df_copy.at[index, 'TMIN'] = None
    return df_copy


def fill_missing_TMIN():
    folder_path = 'data/processed/Algeria'
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            df = fill_missing_TMIN_with_prev_mean(df)  # Use the modified function here
            df.to_csv(file_path, index=False)
            print(f"Missing values in 'TMIN' have been replaced by the mean of the previous 5 days in '{file_name}'.")



