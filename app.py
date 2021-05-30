#import dependencies
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#Setup db and table references
engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)


#Establish routes for Flask
@app.route("/")
def home():
    return(
        f"Available routes:<br/>"
        f"Precipitation data for most recent year: /api/v1.0/precipitation<br/>"
        f"Station list: /api/v1.0/stations<br/>"
        f"Temperature data for most recent year: /api/v1.0/tobs<br/>"
        f"Temperature stats from a start date(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd<br/>"
        f"Temperature stats from a start to end date(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"  
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>="2016-08-23").all()
    
    session.close()

    precip = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["Date"] = date
        precip_dict["Precipitation"] = prcp
        precip.append(precip_dict)
    
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).order_by(Station.station).all()

    session.close()

    station_list = list(np.ravel(results))

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.date,  Measurement.tobs,Measurement.prcp).\
                filter(Measurement.date >= '2016-08-23').filter(Measurement.station=='USC00519281').order_by(Measurement.date).all()

    session.close()

    temps = []
    for date, tobs, prcp in results:
        temps_dict = {}
        temps_dict["Date"] = date
        temps_dict["Temperature"] = tobs
        temps_dict["Precipitation"] = prcp
        temps.append(temps_dict)
    
    return jsonify(temps)


@app.route("/api/v1.0/<start_date>")
def start(start_date):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date>=start_date).all()
    
    session.close()

    start_stats = []
    for min, max, avg in results:
        start_stats_dict = {}
        start_stats_dict["Minimum Temperature"] = min
        start_stats_dict["Maximum Temperature"] = max
        start_stats_dict["Average Temperature"] = avg
        start_stats.append(start_stats_dict)
    
    return jsonify(start_stats)

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date, end_date):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date>=start_date).filter(Measurement.date<=end_date).all()

    session.close()

    end_stats = []
    for min, max, avg in results:
        end_stats_dict = {}
        end_stats_dict["Minimum Temperature"] = min
        end_stats_dict["Maximum Temperature"] = max
        end_stats_dict["Average Temperature"] = avg
        end_stats.append(end_stats_dict)
    
    return jsonify(end_stats)

if __name__ == "__main__":
    app.run(debug=True)