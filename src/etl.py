import os
from utils import *
import pandas as pd
#! uncomment what u want to run
# TODO : make sure to change the folder_path in utils.js to your own after adding the Moroco and tunisia folders in preprocessed folder  
# drop_TAVG_TAVG_ATTRIBUTES()

# fill_missing_TMIN()
# fill_missing_TMIN()

# fill_missing_TMAX()
# fill_missing_TMAX_prev()

# fill_missing_PRCP()
# fill_missing_PRCP_prev()

# fill_TMIN_ATTRIBUTES()
# fill_TMIN_ATTRIBUTES_prev()

# fill_TMAX_ATTRIBUTES()
# fill_TMAX_ATTRIBUTES_prev()

fill_PRCP_ATTRIBUTES()
fill_PRCP_ATTRIBUTES_prev()

def sum_nan_values(folder_path):
    nan_values_sum = {}
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            nan_values_sum[file_name] = {
                # 'TMIN_ATTRIBUTES': df['TMIN_ATTRIBUTES'].isnull().sum(),
                # 'TMAX_ATTRIBUTES': df['TMAX_ATTRIBUTES'].isnull().sum(),
                'PRCP_ATTRIBUTES': df['PRCP_ATTRIBUTES'].isnull().sum(),

            }
    return nan_values_sum

# Example usage:
folder_path = 'data/processed/Algeria'
nan_values_sum = sum_nan_values(folder_path)
for file_name, nan_counts in nan_values_sum.items():
    print(f"File: {file_name}")
    # print(f"NaN values in 'TMIN_ATTRIBUTES': {nan_counts['TMIN_ATTRIBUTES']}")
    # print(f"NaN values in 'TMAX_ATTRIBUTES': {nan_counts['TMAX_ATTRIBUTES']}")
    print(f"NaN values in 'PRCP_ATTRIBUTES': {nan_counts['PRCP_ATTRIBUTES']}")


