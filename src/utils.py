import os
import pandas as pd

#* Function that drops columns
def drop_columns(folder_path, columns_to_drop):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path,low_memory=False)
            # Check if the columns to drop exist in the DataFrame
            columns_exist = all(col in df.columns for col in columns_to_drop)
            if columns_exist:
                # Drop the specified columns
                df.drop(columns=columns_to_drop, inplace=True)
                # Save the modified DataFrame to the processed folder
                processed_folder_path = os.path.join('data', 'processed', os.path.basename(folder_path))
                os.makedirs(processed_folder_path, exist_ok=True)
                processed_file_path = os.path.join(processed_folder_path, file_name)
                df.to_csv(processed_file_path, index=False)
                print(f"{', '.join(columns_to_drop)} columns dropped and file saved: {processed_file_path}")
            else:
                print(f"At least one of the specified columns ({', '.join(columns_to_drop)}) not found in file: {file_name}")

def drop_TAVG_TAVG_ATTRIBUTES(folder_path):
    # Define the columns to drop
    columns_to_drop = ['TAVG','TAVG_ATTRIBUTES']
    drop_columns(folder_path, columns_to_drop)


def drop_columns_if_not_exist(file_path):
    df = pd.read_csv(file_path,low_memory=False)
   # Define the columns to drop
    columns_to_drop = [
        'TAVG', 'TAVG_ATTRIBUTES', 
        "WDFG", "WDFG_ATTRIBUTES", 
        "WDFM", "WDFM_ATTRIBUTES", 
        "WSFG", "WSFG_ATTRIBUTES", 
        "WSFM", "WSFM_ATTRIBUTES", 
        "WT01", "WT01_ATTRIBUTES", 
        "WT02", "WT02_ATTRIBUTES", 
        "WT03", "WT03_ATTRIBUTES", 
        "WT05", "WT05_ATTRIBUTES", 
        "WT07", "WT07_ATTRIBUTES", 
        "WT08", "WT08_ATTRIBUTES", 
        "WT09", "WT09_ATTRIBUTES", 
        "WT16", "WT16_ATTRIBUTES", 
        "WT18", "WT18_ATTRIBUTES",
        "ACSH","ACSH_ATTRIBUTES",
        "PGTM","PGTM_ATTRIBUTES",
        "SNOW","SNOW_ATTRIBUTES",
        "SNWD","SNWD_ATTRIBUTES"
    ]
   
    # Check if each column exists in the DataFrame before dropping
    columns_to_drop_existing = [col for col in columns_to_drop if col in df.columns]
    
    if columns_to_drop_existing:
        df = df.drop(columns=columns_to_drop_existing)
        print(f"Dropped columns: {', '.join(columns_to_drop_existing)}")
        df.to_csv(file_path, index=False)
    if 'SNWD' in df.columns:
        columns_to_drop.append('SNWD')
    if 'SNWD_ATTRIBUTES' in df.columns:
        columns_to_drop.append('SNWD_ATTRIBUTES')
    
    
    return df

def drop_columns_for_all_files(folder_path):
  for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            drop_columns_if_not_exist(file_path)

#* Function that fills missing TMIN

def fill_missing_TMIN_with_next_mean(df):
    # Fill missing values in TMIN column with the mean of the next 5 non-NaN values
 
    df['TMIN'] = df['TMIN'].ffill( limit=20)
    df['TMIN'] = df['TMIN'].bfill(limit=20)
    return df

  

def fill_missing_TMIN(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path, low_memory=False)
            df = fill_missing_TMIN_with_next_mean(df)
            df.to_csv(file_path, index=False)
            print(f"Missing values in 'TMIN' have been replaced by the mean of the next 5 days in '{file_name}'.")

# Example usage:
# fill_missing_TMIN('data/raw/Morocco')



"""

#* Function that fills missing TMAX
def fill_missing_TMAX_with_next_mean(df):
    # Create a copy of the DataFrame to avoid modifying the original
    df_copy = df.copy()
    # Fill missing values in TMAX column with the mean of the next 5 non-NaN values
    for index, row in df_copy.iterrows():
        if pd.isna(row['TMAX']):
            # Select the next 5 rows after the current index
            next_values = df_copy.loc[index+1:index+5, 'TMAX'].dropna()
            # Check if there are enough non-NaN values in the next 5 rows
            if len(next_values) > 0:
                # Calculate the mean of the next non-NaN values and fill the missing value
                df_copy.at[index, 'TMAX'] = round(next_values.mean(), 1)
            else:
                # If there are not enough non-NaN values in the next 5 rows, continue searching
                offset = 1
                while len(next_values) == 0 and index+offset < len(df_copy):
                    next_values = df_copy.loc[index+offset:index+offset+5, 'TMAX'].dropna()
                    offset += 1
                # If non-NaN values are found, calculate the mean and fill the missing value
                if len(next_values) > 0:
                    df_copy.at[index, 'TMAX'] = next_values.mean()
                # If there are still no non-NaN values, fill with NaN
                else:
                    df_copy.at[index, 'TMAX'] = None
    return df_copy

"""
def fill_missing_TMAX():
    folder_path = 'data/raw/Morocco'
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            df = fill_missing_TMAX_with_next_mean(df)  
            df.to_csv(file_path, index=False)
            print(f"Missing values in 'TMAX' have been replaced by the mean of the next 5 days in '{file_name}'.")

def fill_missing_TMAX_with_next_mean(df):
    df_copy = df.copy()
    for index, row in df_copy.iterrows():
        if pd.isna(row['TMAX']):
            next_values = df_copy.loc[index+1:index+25, 'TMAX'].dropna()
            if not next_values.empty:
                df_copy.at[index, 'TMAX'] = round(next_values.mean(), 1)
    return df_copy

def fill_missing_TMAX_with_prev_mean(df):
    df_copy = df.copy()
    for index, row in df_copy.iterrows():
        if pd.isna(row['TMAX']):
            prev_values = df_copy.loc[max(0, index-25):index-1, 'TMAX'].dropna()
            if not prev_values.empty:
                df_copy.at[index, 'TMAX'] = round(prev_values.mean(), 1)
    return df_copy
def fill_missing_PRCP_with_next_non_nan(df):
    df_copy = df.copy()
    df_copy['PRCP'] = df_copy['PRCP'].ffill()
    return df_copy

def fill_missing_PRCP():
    folder_path = 'data/raw/Morocco'
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            df = fill_missing_PRCP_with_next_non_nan(df)  
            df.to_csv(file_path, index=False)
            print(f"Missing values in 'PRCP' have been replaced by next non-NaN value in '{file_name}'.")

def fill_missing_PRCP_with_prev_non_nan(df):
    df_copy = df.copy()
    df_copy['PRCP'] = df_copy['PRCP'].bfill()
    return df_copy

def fill_missing_PRCP_prev():
    folder_path = 'data/raw/Morocco'
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            df = fill_missing_PRCP_with_prev_non_nan(df)  
            df.to_csv(file_path, index=False)
            print(f"Missing values in 'PRCP' have been replaced by previous non-NaN value in '{file_name}'.")


def fill_missing_TMIN_ATTRIBUTES(df):
    df_copy = df.copy()
    df_copy['TMIN_ATTRIBUTES'] = df_copy['TMIN_ATTRIBUTES'].ffill()
    return df_copy

def fill_TMIN_ATTRIBUTES():
    folder_path = 'data/raw/Morocco'
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            df = fill_missing_TMIN_ATTRIBUTES(df)  
            df.to_csv(file_path, index=False)
            print(f"Missing values in 'TMIN_ATTRIBUTES' have been replaced by next non-NaN value in '{file_name}'.")


def fill_missing_TMAX_ATTRIBUTES(df):
    df_copy = df.copy()
    df_copy['TMAX_ATTRIBUTES'] = df_copy['TMAX_ATTRIBUTES'].ffill()
    return df_copy

def fill_TMAX_ATTRIBUTES():
    folder_path = 'data/raw/Morocco'
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            df = fill_missing_TMAX_ATTRIBUTES(df)  
            df.to_csv(file_path, index=False)
            print(f"Missing values in 'TMAX_ATTRIBUTES' have been replaced by next non-NaN value in '{file_name}'.")
def fill_missing_TMIN_ATTRIBUTES_prev(df):
    df_copy = df.copy()
    df_copy['TMIN_ATTRIBUTES'] = df_copy['TMIN_ATTRIBUTES'].bfill()
    return df_copy

def fill_TMIN_ATTRIBUTES_prev():
    folder_path = 'data/raw/Morocco'
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            df = fill_missing_TMIN_ATTRIBUTES_prev(df)  
            df.to_csv(file_path, index=False)
            print(f"Missing values in 'TMIN_ATTRIBUTES' have been replaced by previous non-NaN value in '{file_name}'.")


def fill_missing_TMAX_ATTRIBUTES_prev(df):
    df_copy = df.copy()
    df_copy['TMAX_ATTRIBUTES'] = df_copy['TMAX_ATTRIBUTES'].bfill()
    return df_copy

def fill_TMAX_ATTRIBUTES_prev():
    folder_path = 'data/raw/Morocco'
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            df = fill_missing_TMAX_ATTRIBUTES_prev(df)  
            df.to_csv(file_path, index=False)
            print(f"Missing values in 'TMAX_ATTRIBUTES' have been replaced by previous non-NaN value in '{file_name}'.")
def fill_missing_PRCP_ATTRIBUTES_prev(df):
    df_copy = df.copy()
    df_copy['PRCP_ATTRIBUTES'] = df_copy['PRCP_ATTRIBUTES'].bfill()
    return df_copy

def fill_PRCP_ATTRIBUTES_prev():
    folder_path = 'data/raw/Morocco'
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            df = fill_missing_PRCP_ATTRIBUTES_prev(df)  
            df.to_csv(file_path, index=False)
            print(f"Missing values in 'PRCP_ATTRIBUTES' have been replaced by previous non-NaN value in '{file_name}'.")


def fill_missing_PRCP_ATTRIBUTES(df):
    df_copy = df.copy()
    df_copy['PRCP_ATTRIBUTES'] = df_copy['PRCP_ATTRIBUTES'].ffill()
    return df_copy

def fill_PRCP_ATTRIBUTES():
    folder_path = 'data/raw/Morocco'
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            df = fill_missing_PRCP_ATTRIBUTES(df)  
            df.to_csv(file_path, index=False)
            print(f"Missing values in 'PRCP_ATTRIBUTES' have been replaced by next non-NaN value in '{file_name}'.")



def find_missing_values(df, column_name):
    # Boolean indexing to filter rows with missing values in the specified column
    missing_rows = df[df[column_name].isna()]
    return missing_rows


def drop_rows_with_null_values(df):
    df_without_null = df.dropna()
    return df_without_null


