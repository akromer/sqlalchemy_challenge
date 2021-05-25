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

# Measurement = Base.classes.measurement
# Station = Base.classes.station

app = Flask(__name__)


#Establish routes for Flask
@app.route("/")
def home():
    return(
        f"Available routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"Stations: /api/v1.0/stations<br/>"
        f"Temperature for most recent year: /api/v1.0/tobs<br/>"
        f"Temperature stats from a start date(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd<br/>"
        f"Temperature stats from a start to end date(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"  
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date)


    session.close()

# @app.route("/api/v1.0/stations")
# def stations():

# @app.route("/api/v1.0/tobs")
# def tobs():

# @app.route("")
# def start():

# @app.route("")
# def start_end():

if __name__ == "__main__":
    app.run(debug=True)