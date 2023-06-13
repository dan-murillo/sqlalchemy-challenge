# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
#from flask_cors import CORS

#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

# Defined a function to find the year before; the function is used in the precipitation and temperature routes:
def the_year_before():
    most_recent_datapoint = session.query(func.max(measurement.date)).scalar()
    reformatted_most_recent_datapoint = dt.datetime.strptime(most_recent_datapoint, '%Y-%m-%d').date()
    one_year_before = reformatted_most_recent_datapoint - dt.timedelta(days=365)
    return (one_year_before)

#################################################
# Flask Setup
#################################################

# Created an app to pass __name__:
app = Flask(__name__)
#CORS(app)


#################################################
# Flask Routes
#################################################

# Homepage route:
@app.route('/')
def homepage():
    print("The server received a request for the homepage...")
    return (
        f"<h1>Welcome to the API for <i>my Hawaiian Holiday</i>!</h1><br/>"
        f"/api/v1.0/precipitation <- <i>This route leads to ????</i><br/>"
        f"/api/v1.0/stations <- <i>This route has ????</i><br/>"
        f"/api/v1.0/tobs <- <i>This route takes you to ????</i><br/>"
        f"/api/v1.0/<start> <- <i>This route gets you to ????</i><br/>"
        f"/api/v1.0/<start>/<end> <- <i>This route leads to ??? </i><br/>"
    )

# Precipitation query route:
@app.route('/api/v1.0/precipitation')
def precipitation_query():
    last_year_precipitation_scores_l = session.query(measurement.date, measurement.prcp).filter(measurement.date > the_year_before()).all()
    last_year_precipitation_scores_d = dict(last_year_precipitation_scores_l)
    session.close()
    return jsonify(last_year_precipitation_scores_d)
    
# Stations query route:
@app.route('/api/v1.0/stations')
def stations_query():
    station = Base.classes.station
    stations_l = session.query(station.id, station.station, station.name, station.latitude, station.longitude, station.elevation).all()
    stations_d = []
    for id, station, name, latitude, longitude, elevation in stations_l:
        stations_temp_d = {}
        stations_temp_d['id'] = id
        stations_temp_d['station'] = station
        stations_temp_d['name'] = name
        stations_temp_d['latitude'] = latitude
        stations_temp_d['longitude'] = longitude
        stations_temp_d['elevation'] = elevation
        stations_d.append(stations_temp_d)
    session.close()
    return jsonify(stations_d)

# Temperatures query route:
@app.route('/api/v1.0/tobs')
def temperatures_query():
    most_active_stations_a = session.query(measurement.station, func.count(measurement.date)).group_by(measurement.station).order_by(func.sum(measurement.station).desc()).all()
    sorted_most_active_stations_a = sorted(most_active_stations_a, key=lambda x: -x[1])
    most_active_station = sorted_most_active_stations_a[0][0]
    last_year_temperature_data_most_active_station_l = session.query(measurement.date, measurement.tobs).filter(measurement.date > the_year_before()).filter(measurement.station == most_active_station).all()
    last_year_temperature_data_most_active_station_d = dict(last_year_temperature_data_most_active_station_l)
    session.close()
    return(last_year_temperature_data_most_active_station_d)



# To run the app:
if __name__ == "__main__":
    app.run(debug=True)
    