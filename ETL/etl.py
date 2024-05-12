import os
from ETL.utils.utils_AG import *
from ETL.utils.utils_MO_TS import *
import pandas as pd

#? uncomment what u want to run
# drop_TAVG_TAVG_ATTRIBUTES()

# fill_missing_TMIN()

# fill_missing_TMAX()

# fill_missing_PRCP()

# fill_TMIN_ATTRIBUTES()

# fill_TMAX_ATTRIBUTES()

# fill_PRCP_ATTRIBUTES()

# usage example :
folder_path = 'data/processed/Algeria'
drop_columns_for_all_files(folder_path)
