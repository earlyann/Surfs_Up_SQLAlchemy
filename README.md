# SQLAlchemy_Challenge

## Climate Analysis of Honolulu, Hawaii

### Project Overview
The goal of this project is to perform a basic climate analysis and data exploration of a SQLite climate database for Honolulu, Hawaii. The analysis is performed using Python and SQLAlchemy ORM queries, Pandas, and Matplotlib.

In the first part of the project, Python and SQLAlchemy are used to analyze and explore the climate data. SQLAlchemy is used to connect to the SQLite database, reflect the tables into classes, and link Python to the database by creating a SQLAlchemy session. The precipitation and station analyses are performed by querying the most current 12 months of data from the most current date in the dataset for precipitation and temperature data. The results are then loaded into a Pandas DataFrame and plotted.

In the second part of the project, a Flask API is designed based on the queries from the first part of the project. The API routes are designed to return JSON data for precipitation, stations, temperature observations, and temperature statistics for a specified start or start-end range.

#### Methods Used
- Data exploration
- Data analysis
- Data visualization
- Web development
- API design

#### Technologies
- Flask
- Python
- SQLAlchemy
- SQLite
- Pandas
- Matplotlib

### Outputs
The outputs of this project are a Flask API that provides JSON data for precipitation, stations, temperature observations, and temperature statistics for a specified start or start-end range and a notebooke containing the exploration and analysis, including precipitation and temperature observation data are plots using Matplotlib to provide a visual representation of the data.
