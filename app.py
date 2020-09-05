import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


# Engine, reflect, reference
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)
app = Flask(__name__)


# Home page
@app.route("/")
def home():
    return (
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
    )



@app.route("/api/v1.0/precipitation")
def precip():

    # Create session and query results
    session = Session(engine)
    """Precipitation data"""
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

 
    # Create dictionary, create list of dictionaries, jsonify
    precipitation = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict[date] = prcp
        precipitation.append(precip_dict)

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():

    # Create session and query results
    session = Session(engine)
    """List of Stations"""
    results = session.query(Station.station, Station.name).all()
    session.close()

 
    # Create dictionary, create list of dictionaries, jsonify
    stations = []
    for station, name in results:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        stations.append(station_dict)

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def temp():

    # Create session and query results
    session = Session(engine)
    """Temperature data"""
    
    # Last year of data
    lastdatestring = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    lastdate = dt.datetime.strptime(lastdatestring[0],'%Y-%m-%d')
    last_data_date = lastdate - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= last_data_date).all()
    session.close()

 
    # Create dictionary, create list of dictionaries, jsonify
    temp = []
    for date, tobs in results:
        temp_dict = {}
        temp_dict[date] = tobs
        temp.append(temp_dict)

    return jsonify(temp)


@app.route("/api/v1.0/<start>")
def start(start):

    # Create session and query results
    session = Session(engine)
    """Data range"""

    # User input date
    startdate = dt.datetime.strptime(start,'%Y-%m-%d')
    
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= startdate).all()
    session.close()

 
    # Create dictionary, create list of dictionaries, jsonify
    datalist = []
    for date, min, avg, max in results:
        data_dict = {}
        data_dict["Date"] = date
        data_dict["TMin"] = min
        data_dict["TAvg"] = avg
        data_dict["TMax"] = max
        datalist.append(data_dict)

    return jsonify(datalist)

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):

    # Create session and query results
    session = Session(engine)
    """Data range"""

    # User input date
    startdate = dt.datetime.strptime(start,'%Y-%m-%d')
    enddate = dt.datetime.strptime(end,'%Y-%m-%d')
    
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
              filter(Measurement.date >= startdate, Measurement.date <= enddate).all()
    session.close()

 
    # Create dictionary, create list of dictionaries, jsonify
    datalist = []
    for date, min, avg, max in results:
        data_dict = {}
        data_dict["Date"] = date
        data_dict["TMin"] = min
        data_dict["TAvg"] = avg
        data_dict["TMax"] = max
        datalist.append(data_dict)

    return jsonify(datalist)





if __name__ == "__main__":
    app.run(debug=True)
