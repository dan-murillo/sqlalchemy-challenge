# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
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
    most_recent_datapoint = session.query(func.max(measurement.date)).scalar()
    reformatted_most_recent_datapoint = dt.datetime.strptime(most_recent_datapoint, '%Y-%m-%d').date()
    one_year_before = reformatted_most_recent_datapoint - dt.timedelta(days=365)
    last_year_precipitation_scores_l = session.query(measurement.date, measurement.prcp).filter(measurement.date > one_year_before).all()
    






# To run the app:
if __name__ == "__main__":
    app.run(debug=True)
    