import os
from utils import utils_MO_TS
from utils import utils_AG

import pandas as pd

#? uncomment what u want to run
# drop_TAVG_TAVG_ATTRIBUTES()

#fill_missing_TMIN()

#fill_missing_TMAX()

# fill_missing_PRCP()

# fill_TMIN_ATTRIBUTES()

# fill_TMAX_ATTRIBUTES()

# fill_PRCP_ATTRIBUTES()

# usage example :
folder_path = 'data/processed/Tunisia'
#utils_AG.drop_columns_for_all_files(folder_path)
df=pd.read_csv('data/processed/Tunisia/Weather_2020-2022_TUNISIA.csv') 
print(df.info())

