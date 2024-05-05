import os
from utils import *
import pandas as pd
#! uncomment what u want to run
# TODO : make sure to change the folder_path in utils.js to your own after adding the Moroco and tunisia folders in preprocessed folder  
# ? All algeria data 100% cleaned 
# drop_TAVG_TAVG_ATTRIBUTES()
folder_path = 'data/raw/Morocco'
fill_missing_TMIN(folder_path)


fill_missing_TMAX()
# fill_missing_TMAX_prev()

# fill_missing_PRCP()
# fill_missing_PRCP_prev()

# fill_TMIN_ATTRIBUTES()
# fill_TMIN_ATTRIBUTES_prev()

# fill_TMAX_ATTRIBUTES()
# fill_TMAX_ATTRIBUTES_prev()

# fill_PRCP_ATTRIBUTES()
# fill_PRCP_ATTRIBUTES_prev()


drop_columns_for_all_files(folder_path)
df=pd.read_csv('data/raw/Morocco/Weather_1990-2019_MOROCCO.csv',low_memory=False)
df2=pd.read_csv('data/raw/Morocco/Weather_2020-2022_MOROCCO.csv',low_memory=False)
print(df.info())
print(df2.info())

df = drop_rows_with_null_values(df)
print(df)