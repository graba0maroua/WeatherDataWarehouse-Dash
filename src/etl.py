import os
from utils import drop_columns

# Define the folder path
folder_path = os.path.join('data', 'raw', 'Algeria')
# Define the columns to drop
columns_to_drop = ['TAVG', 'TAVG_ATTRIBUTES']
# Call the function from utils.py to drop the specified columns from all CSV files in the folder
drop_columns(folder_path, columns_to_drop)
