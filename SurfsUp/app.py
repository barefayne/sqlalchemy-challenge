import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


# #################################################
# # Flask Routes
# #################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of all precipitation"""
    # Query all precipitation
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-24").all()

    session.close()

# Convert the list to Dictionary
    year_prcp = []
    for date,prcp  in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp     
        year_prcp.append(prcp_dict)

    return jsonify(year_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(Measurement.station, func.count(Measurement.id)).\
            group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).all()
    
    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)
    

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of tobs"""
    # Query the last 12 months of temperature observation data for the most active station
    results = session.query(Measurement.station, Measurement.prcp, Measurement.date,Measurement.tobs)\
    .filter(Measurement.date >= '2016-08-23')\
    .filter(Measurement.station == 'USC00519281')\
    .all()
   
    session.close()

     # Convert the list to Dictionary
    all_tobs = []
    for station,prcp, date,tobs in results:
        tobs_dict = {}
        tobs_dict["station"] = station
        tobs_dict["prcp"] = prcp
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)


if __name__ == '__main__':
    app.run(debug=True)
