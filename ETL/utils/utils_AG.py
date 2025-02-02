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


def drop_columns_if_not_exist(file_path):
    df = pd.read_csv(file_path)
    columns_to_drop = []
    if 'SNWD' in df.columns:
        columns_to_drop.append('SNWD')
    if 'SNWD_ATTRIBUTES' in df.columns:
        columns_to_drop.append('SNWD_ATTRIBUTES')
    
    if columns_to_drop:
        df = df.drop(columns=columns_to_drop)
        print(f"Dropped columns: {', '.join(columns_to_drop)}")
        df.to_csv(file_path, index=False)
    
    return df

def drop_columns_for_all_files(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            drop_columns_if_not_exist(file_path)

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


def fill_missing_TMIN():
    folder_path = 'data/processed/Algeria'
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            df = fill_missing_TMIN_with_next_mean(df)  # Use the modified function here
            df.to_csv(file_path, index=False)
            print(f"Missing values in 'TMIN' have been replaced by the mean of the next 5 days in '{file_name}'.")





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


def fill_missing_TMAX():
    folder_path = 'data/processed/Algeria'
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            df = fill_missing_TMAX_with_next_mean(df)  
            df.to_csv(file_path, index=False)
            print(f"Missing values in 'TMAX' have been replaced by the mean of the next 5 days in '{file_name}'.")


def fill_missing_TMAX_with_prev_mean(df):
    df_copy = df.copy()
    for index, row in df_copy.iterrows():
        if pd.isna(row['TMAX']):
            prev_values = df_copy.loc[max(0, index-5):index-1, 'TMAX'].dropna()
            if len(prev_values) > 0:
                df_copy.at[index, 'TMAX'] = round(prev_values.mean(), 1)  # Round to 1 decimal place
            else:
                offset = 1
                while len(prev_values) == 0 and index+offset < len(df_copy):
                    prev_values = df_copy.loc[max(0, index-offset-5):index-offset-1, 'TMAX'].dropna()
                    offset += 1
                if len(prev_values) > 0:
                    df_copy.at[index, 'TMAX'] = round(prev_values.mean(), 1)  # Round to 1 decimal place
                else:
                    df_copy.at[index, 'TMAX'] = None
    return df_copy

def fill_missing_TMAX_prev():
    folder_path = 'data/processed/Algeria'
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            df = fill_missing_TMAX_with_prev_mean(df)  
            df.to_csv(file_path, index=False)
            print(f"Missing values in 'TMAX' have been replaced by the mean of the prev 5 days in '{file_name}'.")

def fill_missing_PRCP_with_next_non_nan(df):
    df_copy = df.copy()
    for index, row in df_copy.iterrows():
        if pd.isna(row['PRCP']):
            next_index = index + 1
            while next_index < len(df_copy):
                next_value = df_copy.at[next_index, 'PRCP']
                if not pd.isna(next_value):
                    df_copy.at[index, 'PRCP'] = next_value
                    break
                next_index += 1
            else:
                # If no non-NaN value is found, set the current value to NaN
                df_copy.at[index, 'PRCP'] = None
    return df_copy



def fill_missing_PRCP():
    folder_path = 'data/processed/Algeria'
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            df = fill_missing_PRCP_with_next_non_nan(df)  
            df.to_csv(file_path, index=False)
            print(f"Missing values in 'PRCP' have been replaced by next Non nan value '{file_name}'.") 


def fill_missing_PRCP_with_prev_non_nan(df):
    df_copy = df.copy()
    for index, row in df_copy.iterrows():
        if pd.isna(row['PRCP']):
            prev_index = index - 1
            while prev_index >= 0:
                prev_value = df_copy.at[prev_index, 'PRCP']
                if not pd.isna(prev_value):
                    df_copy.at[index, 'PRCP'] = prev_value
                    break
                prev_index -= 1
            else:
                # If no non-NaN value is found, set the current value to NaN
                df_copy.at[index, 'PRCP'] = None
    return df_copy

def fill_missing_PRCP_prev():
    folder_path = 'data/processed/Algeria'
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            df = fill_missing_PRCP_with_prev_non_nan(df)  
            df.to_csv(file_path, index=False)
            print(f"Missing values in 'PRCP' have been replaced by previous Non-NaN value in '{file_name}'.")



def fill_missing_TMIN_ATTRIBUTES(df):
    df_copy = df.copy()
    for index, row in df_copy.iterrows():
        if pd.isna(row['TMIN_ATTRIBUTES']):
            next_index = index + 1
            while next_index < len(df_copy):
                next_value = df_copy.at[next_index, 'TMIN_ATTRIBUTES']
                if not pd.isna(next_value):
                    df_copy.at[index, 'TMIN_ATTRIBUTES'] = next_value
                    break
                next_index += 1
            else:
                # If no non-NaN value is found, set the current value to NaN
                df_copy.at[index, 'TMIN_ATTRIBUTES'] = None
    return df_copy


def fill_TMIN_ATTRIBUTES():
    folder_path = 'data/processed/Algeria'
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            df = fill_missing_TMIN_ATTRIBUTES(df)  
            df.to_csv(file_path, index=False)
            print(f"Missing values in 'TMIN_ATTRIBUTES' have been replaced by next Non nan value '{file_name}'.") 

def fill_missing_TMAX_ATTRIBUTES(df):
    df_copy = df.copy()
    for index, row in df_copy.iterrows():
        if pd.isna(row['TMAX_ATTRIBUTES']):
            next_index = index + 1
            while next_index < len(df_copy):
                next_value = df_copy.at[next_index, 'TMAX_ATTRIBUTES']
                if not pd.isna(next_value):
                    df_copy.at[index, 'TMAX_ATTRIBUTES'] = next_value
                    break
                next_index += 1
            else:
                # If no non-NaN value is found, set the current value to NaN
                df_copy.at[index, 'TMAX_ATTRIBUTES'] = None
    return df_copy


def fill_TMAX_ATTRIBUTES():
    folder_path = 'data/processed/Algeria'
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            df = fill_missing_TMAX_ATTRIBUTES(df)  
            df.to_csv(file_path, index=False)
            print(f"Missing values in 'TMAX_ATTRIBUTES' have been replaced by next Non nan value '{file_name}'.") 

def fill_missing_TMAX_ATTRIBUTES_prev(df):
    df_copy = df.copy()
    for index, row in df_copy.iterrows():
        if pd.isna(row['TMAX_ATTRIBUTES']):
            prev_index = index - 1
            while prev_index >= 0:
                prev_value = df_copy.at[prev_index, 'TMAX_ATTRIBUTES']
                if not pd.isna(prev_value):
                    df_copy.at[index, 'TMAX_ATTRIBUTES'] = prev_value
                    break
                prev_index -= 1
            else:
                # If no non-NaN value is found, set the current value to NaN
                df_copy.at[index, 'TMAX_ATTRIBUTES'] = None
    return df_copy

def fill_TMAX_ATTRIBUTES_prev():
    folder_path = 'data/processed/Algeria'
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            df = fill_missing_TMAX_ATTRIBUTES_prev(df)  
            df.to_csv(file_path, index=False)
            print(f"Missing values in 'TMAX_ATTRIBUTES' have been replaced by previous Non nan value '{file_name}'.") 


def fill_missing_TMIN_ATTRIBUTES_prev(df):
    df_copy = df.copy()
    for index, row in df_copy.iterrows():
        if pd.isna(row['TMIN_ATTRIBUTES']):
            prev_index = index - 1
            while prev_index >= 0:
                prev_value = df_copy.at[prev_index, 'TMIN_ATTRIBUTES']
                if not pd.isna(prev_value):
                    df_copy.at[index, 'TMIN_ATTRIBUTES'] = prev_value
                    break
                prev_index -= 1
            else:
                # If no non-NaN value is found, set the current value to NaN
                df_copy.at[index, 'TMIN_ATTRIBUTES'] = None
    return df_copy

def fill_TMIN_ATTRIBUTES_prev():
    folder_path = 'data/processed/Algeria'
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            df = fill_missing_TMIN_ATTRIBUTES_prev(df)  
            df.to_csv(file_path, index=False)
            print(f"Missing values in 'TMIN_ATTRIBUTES' have been replaced by previous Non nan value '{file_name}'.") 



def fill_missing_PRCP_ATTRIBUTES_prev(df):
    df_copy = df.copy()
    for index, row in df_copy.iterrows():
        if pd.isna(row['PRCP_ATTRIBUTES']):
            prev_index = index - 1
            while prev_index >= 0:
                prev_value = df_copy.at[prev_index, 'PRCP_ATTRIBUTES']
                if not pd.isna(prev_value):
                    df_copy.at[index, 'PRCP_ATTRIBUTES'] = prev_value
                    break
                prev_index -= 1
            else:
                # If no non-NaN value is found, set the current value to NaN
                df_copy.at[index, 'PRCP_ATTRIBUTES'] = None
    return df_copy

def fill_PRCP_ATTRIBUTES_prev():
    folder_path = 'data/processed/Algeria'
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            df = fill_missing_PRCP_ATTRIBUTES_prev(df)  
            df.to_csv(file_path, index=False)
            print(f"Missing values in 'PRCP_ATTRIBUTES' have been replaced by previous Non nan value '{file_name}'.") 


def fill_missing_PRCP_ATTRIBUTES(df):
    df_copy = df.copy()
    for index, row in df_copy.iterrows():
        if pd.isna(row['PRCP_ATTRIBUTES']):
            next_index = index + 1
            while next_index < len(df_copy):
                next_value = df_copy.at[next_index, 'PRCP_ATTRIBUTES']
                if not pd.isna(next_value):
                    df_copy.at[index, 'PRCP_ATTRIBUTES'] = next_value
                    break
                next_index += 1
            else:
                # If no non-NaN value is found, set the current value to NaN
                df_copy.at[index, 'PRCP_ATTRIBUTES'] = None
    return df_copy


def fill_PRCP_ATTRIBUTES():
    folder_path = 'data/processed/Algeria'
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            df = fill_missing_PRCP_ATTRIBUTES(df)  
            df.to_csv(file_path, index=False)
            print(f"Missing values in 'PRCP_ATTRIBUTES' have been replaced by next Non nan value '{file_name}'.") 
