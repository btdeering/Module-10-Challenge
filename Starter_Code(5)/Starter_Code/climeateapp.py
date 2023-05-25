# Import the dependencies.
import numpy as np
import datetime as dt
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


#################################################
# Database Setup
#################################################
# Create the connection engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()
base.prepare(engine, reflect=True)
# reflect the tables
base.classes.keys()

# Save references to each table
Measurement = base.classes.measurement
Station = base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
# Import Flask
from flask import Flask, jsonify

# Create an app
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
# Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to my 'Home' page!"

# Define what to do when a user hits the /about route
@app.route("/about")
def about():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"

# Define what to do when a user hits the /precipitation route
@app.route("/precipitation")
def precipitation():
    print("Server received request for 'Precipitation' page...")
    # Query for the dates and precipitation observations from the last year.
    # Convert the query results to a Dictionary using date as the key and prcp as the value.
    # Return the json representation of your dictionary.
    # Query for the dates and precipitation observations from the last year.
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= last_year).all()

    # Create a dictionary from the row data and append to a list of for the precipitation data
    precipitation_data = []
    for result in results:
        row = {}
        row["date"] = result[0]
        row["prcp"] = result[1]
        precipitation_data.append(row)

    return jsonify(precipitation_data)

# Define what to do when a user hits the /stations route
@app.route("/stations")
def stations():
    print("Server received request for 'Stations' page...")
    # Return a json list of stations from the dataset.
    # Query all stations
    results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(results))

    return jsonify(station_list)

# Define what to do when a user hits the /tobs route
@app.route("/tobs")
def tobs():
    print("Server received request for 'Tobs' page...")
    # Return a json list of Temperature Observations (tobs) for the previous year.
    # Query for the dates and temperature observations from the last year.
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= last_year).all()

    # Create a dictionary from the row data and append to a list of for the temperature data
    temperature_data = []
    for result in results:
        row = {}
        row["date"] = result[0]
        row["tobs"] = result[1]
        temperature_data.append(row)

    return jsonify(temperature_data)

# Define what to do when a user hits the /<start> route
@app.route("/<start>")
def start(start):
    print("Server received request for 'Start' page...")
    # Return a json list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    # Query for the dates and temperature observations from the last year.
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= start).all()

    # Create a dictionary from the row data and append to a list of for the temperature data
    temperature_data = []
    for result in results:
        row = {}
        row["date"] = result[0]
        row["tobs"] = result[1]
        temperature_data.append(row)

    return jsonify(temperature_data)

# Define what to do when a user hits the /<start>/<end> route
@app.route("/<start>/<end>")
def start_end(start, end):
    print("Server received request for 'Start/End' page...")
    # Return a json list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    # Query for the dates and temperature observations from the last year.
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    # Create a dictionary from the row data and append to a list of for the temperature data
    temperature_data = []
    for result in results:
        row = {}
        row["date"] = result[0]
        row["tobs"] = result[1]
        temperature_data.append(row)

    return jsonify(temperature_data)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)