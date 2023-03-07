# 1. import Flask
from flask import Flask, jsonify
import datetime as dt
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Creating engine to hawaii.sqlite
engine = create_engine("sqlite:////Users/laceymorgan/Desktop/SQLAlchemy_Challenge/Resources/hawaii.sqlite")

# Reflecting  the database
Base = automap_base()
Base.prepare(autoload_with=engine)

# Saving variable references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Creating the app
app = Flask(__name__)


# Defining the index route, including a list all the available routes.
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (f"Routes available:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/&lt;start&gt;<br>"
            f"/api/v1.0/&lt;start&gt;/&lt;end&gt;")


# Converting the query results from my precipitation analysis, looking at the most current 12 months of data, using date as the key and prcp as the value.
@app.route("/api/v1.0/precipitation")
def precipitation():
    session= Session(engine)

    max_date = session.query(func.max(measurement.date)).scalar()
    query_date = dt.date.fromisoformat(max_date) - dt.timedelta(days=365)

    # Performing a query to retrieve the data and precipitation scores
    results = session.query(measurement.date, measurement.prcp).\
        filter(func.strftime('%Y-%m-%d', measurement.date) >= query_date.strftime('%Y-%m-%d')).all()
    
    session.close()

    # convert tuples into normal list
    annual_prcp = list(np.ravel(results))
    # convert result to json
    return jsonify(annual_prcp)



# Returning a JSON list of stations from the dataset.
@app.route('/api/v1.0/stations')
def stations():
    session= Session(engine)

    # query the database for all station names
    results =  session.query(station.name).all()
    session.close()

    # convert tuples into normal list
    stations = list(np.ravel(results))
    # convert result to json
    return jsonify(stations)



# Quering the dates and temperature observations of the most-active station for the most current year of data, returning json
@app.route('/api/v1.0/tobs')
def tobs():
    session= Session(engine)

    # Query to find the most active stations counts in descending order.
    station_activity = session.query(measurement.station, func.count(measurement.id)).\
                                group_by(measurement.station).\
                                order_by(func.count(measurement.id).desc()).all()
    
    most_active_station = station_activity[0][0]

    max_date = session.query(func.max(measurement.date)).scalar()
    query_date = dt.date.fromisoformat(max_date) - dt.timedelta(days=365)

    # A query to retrieve the data and precipitation scores
    results = session.query(measurement.date, measurement.tobs).\
        filter(func.strftime('%Y-%m-%d', measurement.date) >= query_date.strftime('%Y-%m-%d')).\
        filter(measurement.station == most_active_station).\
        all()
    
    session.close()

     # Creating a list of dictionaries with keys for date and tobs
    tobs_data = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        tobs_data.append(tobs_dict)

    # Return the JSON list of temperature observations for the previous year
    return jsonify(tobs_data)




# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature 
# for a specified start and for all the dates greater than or equal to the start date.
@app.route('/api/v1.0/<start>')
def temp_stats_start(start):    
    session= Session(engine)

    # Perform a query to retrieve the minimum, average, and maximum temperatures
    # for all dates greater than or equal to the specified start date
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()

    session.close()

    # convert tuples into normal list
    temp_stats = list(np.ravel(results))
    # convert result to json
    return jsonify(temp_stats)


# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the 
# start date to the end date, inclusive.           
@app.route('/api/v1.0/<start>/<end>')
def temp_stats_start_stop(start, end):

    session= Session(engine)

    temp_stats = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).\
        all()
    
    session.close()

    # Converting the result to a dictionary with keys for the temperature stats
    temp_dict = {'Minimum Temperature': temp_stats[0][0], 'Average Temperature': temp_stats[0][1], 'Maximum Temperature': temp_stats[0][2]}

    # Return the temperature stats as JSON
    return jsonify(temp_dict)
    
    
if __name__ == "__main__":
    app.run(port=8080, debug=True)
