﻿# WeatherDataWarehouse-Dash

## Description

This repository contains the implementation of a project aimed at transforming raw climate data into a data warehouse. 

## Project Details

Here are the key aspects:

- **Implementation**: Exclusively in Python and MySQL.
- **Star Schema**: A star schema is modelled and stored in a database named "Weather_DataWarehouse".
- **ETL Process**: Data warehouse tables are populated using the ETL process, loading data from flat files into the "Weather_DataWarehouse".
- **Dashboard**: A dashboard is created using Dash under Python, facilitating data analysis.
- **Dynamic Visualization**: The dashboard includes dynamic graphs and charts visualizing the evolution of climate data.

## Dataset Description

The dataset provided by the National Centers for Environmental Information covers climate data from three countries in the Maghreb. It includes the following attributes:

- Precipitation (PRCP)
- Snow Depth (SNWD)
- Snowfall (SNOW)
- Average Temperature (TAVG)
- Maximum Temperature (TMAX)
- Minimum Temperature (TMIN)
- Direction of Maximum Wind Gust (WDFG)
- Peak Gust Time (PGTM)
- Maximum Wind Speed in Gust (WSFG)
- Weather Types (WT**)

In addition to climate data, there are attributes providing information about the station code, its name, geographical position, and the date of sampling.

## Resources

- **Dash Documentation**: [Documentation Dash](link)

