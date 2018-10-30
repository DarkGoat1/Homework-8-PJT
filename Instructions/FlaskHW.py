from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

precip = session.query(Measurement.date,
                      Measurement.prcp).all()

stations = session.query(Station.id,
                       Station.station,
                      Station.name,
                      Station.latitude,
                      Station.longitude,
                       Station.elevation).all()

tobs = session.query(Measurement.date,
                      Measurement.tobs).filter(Measurement.date >= '2016-08-23').all()



# function usage example
# print(calc_temps('2012-02-28', '2012-03-05'))

app = Flask(__name__)

@app.route("/api/v1.0/precipitation")
def home():
    return jsonify(precip)


@app.route("/api/v1.0/stations")
def normal():
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def jsonified():
    return jsonify(tobs)

@app.route("/api/v1.0/date/<start>/<end>")
def datememe(start, end):
    def calc_temps(start_date, end_date):
        engine = create_engine("sqlite:///hawaii.sqlite")

        # reflect an existing database into a new model
        Base = automap_base()
        # reflect the tables
        Base.prepare(engine, reflect=True)

        # Save reference to the table
        Measurement = Base.classes.measurement
        Station = Base.classes.station

        # Create our session (link) from Python to the DB
        session = Session(engine)
        """TMIN, TAVG, and TMAX for a list of dates.
    
        Args:
            start_date (string): A date string in the format %Y-%m-%d
            end_date (string): A date string in the format %Y-%m-%d
        
        Returns:
            TMIN, TAVE, and TMAX
        """
    
        return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    return jsonify(calc_temps(start, end))


if __name__ == "__main__":
    app.run(debug=True, port=2005)