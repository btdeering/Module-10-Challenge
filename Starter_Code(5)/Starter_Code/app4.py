# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

#################################################
# Database Setup
#################################################
# Create an engine to connect to the database
engine = create_engine("sqlite:///C:/Users/btdee/Dropbox/Data Bootcamp/Weekly Challenges/Module 10 Challenge/Starter_Code(5)/Starter_Code/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################


#################################################
# Flask Routes
#################################################
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Perform your precipitation analysis query here (retrieve last 12 months of data)
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-23").\
        filter(Measurement.date <= "2017-08-23").all()

    # Convert the query results to a dictionary using date as the key and prcp as the value
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}

    # Return the JSON representation of the dictionary
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Perform your query to retrieve the list of stations here
    distinct_stations = session.query(Measurement.station).distinct()
    stations_list = [station[0] for station in distinct_stations]
    # Store the results in a list variable (e.g., stations_list)
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Perform your query to retrieve the temperature observations here
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= "2016-08-23").\
        filter(Measurement.date <= "2017-08-23").all()
    tobs_list = [tobs[1] for tobs in tobs_data]
    # Store the results in a list variable (e.g., tobs_list)
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def temperature_range_start(start):
    # Perform your query to calculate the temperature statistics for the specified start date
    temperature_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= "2016-08-23").\
        filter(Measurement.date <= "2017-08-23").all()
    temp_stats_dict = {"min": temperature_data[0][0], "avg": temperature_data[0][1], "max": temperature_data[0][2]}
    # Store the results in a dictionary variable (e.g., temp_stats_dict)
    return jsonify(temp_stats_dict)

@app.route("/api/v1.0/<start>/<end>")
def temperature_range_start_end(start, end):
    # Perform your query to calculate the temperature statistics for the specified start and end dates
    temperature_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= "2016-08-23").\
        filter(Measurement.date <= "2017-08-23").all()
    temp_stats_dict = {"min": temperature_data[0][0], "avg": temperature_data[0][1], "max": temperature_data[0][2]}
    # Store the results in a dictionary variable (e.g., temp_stats_dict)
    return jsonify(temp_stats_dict)

if __name__ == "__main__":
    app.run()
