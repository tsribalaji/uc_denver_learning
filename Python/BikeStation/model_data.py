import pymongo
import datetime
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.text_factory = str
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)


if __name__ == '__main__':
    # Mongo conecction

    db_config = dict(
        connection_string='mongodb+srv://{0}:{1}@cluster0.s5bx2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority',
        user='m001-student', password='m001-mongodb-basics')

    client = pymongo.MongoClient(db_config["connection_string"].format(db_config["user"], db_config["password"]))

    mongo_db = client['BikeStation']
    count = 0 # todo
    for bike_station in mongo_db.BikeStationData.find():
        bike_station_id = bike_station['id']

        isodate = bike_station['timestamp']
        dt = datetime.datetime.fromisoformat(isodate)
        timestamp = datetime.datetime.timestamp(dt)

        # todo -
        station_name = bike_station['station_name']
        total_docks = int(bike_station['total_docks'])
        docks_in_service = int(bike_station['docks_in_service'])
        available_docks = int(bike_station['available_docks'])
        status = bike_station['status']
        record = bike_station['record']
        latitude = float(bike_station['latitude'])
        longitude = float(bike_station['longitude'])
        print(bike_station)
        # todo start
        count += 1
        if count > 10:
            break
        # todo end

    # SQLite connection
    connection = create_connection(r"C:\Users\Balajisri\Desktop\New folder\College\PYTHON\index.sqlite")
    cur = connection.cursor()

    # Each time model_data.py runs - it should completely wipe out and re-build the index.sqlite, database allowing you to adjust its parameters and edit the mapping tables in index.sqlite to tweak the data modeling process.
    cur.executescript('''DROP TABLE IF EXISTS Counts;
                         DROP TABLE IF EXISTS Loc''')

    # It should store the data necessary to create a BikeStation object (Assignment 1) as downloaded from the MongoDB data (Assignment 2)
    cur.executescript('''CREATE TABLE IF NOT EXISTS Counts (recordID INTEGER PRIMARY KEY, 
        timestamp INTEGER,
        stationname TEXT, 
        total_docks INTEGER, 
        docks_in_service INTEGER, 
        available_docks INTEGER, 
        status TEXT, 
        entitystatus TEXT, total_docks TEXT, entityformdate TEXT, year INTEGER);
        CREATE TABLE IF NOT EXISTS Locs 
        (locationId INTEGER PRIMARY KEY AUTOINCREMENT, latitude Text, longitude TEXT, 
        state TEXT, zipcode TEXT, country TEXT)''')
#



         = bike_station['status']
        latitude = float(bike_station['latitude'])
         = float(bike_station['longitude'])
# It should do some validation on the data
# Running model_earthquakes.py can take quite a bit of time because it loops through every earthquake record, extracts relevant fields from the date, it will run faster if you do not write every earthquake to the screen and only commit the earthquake data to write it to the database every 50 to 100 earthquakes.
# The python code in the following lectures that is a good starting point for coding this assignment.
# Example: Python and Databases
# Example: MongoDB and Atlas
# Reading and Writing Data
# You will need to update the SQL queries to create and insert bike station data into a database table called bike_stations - or some other reasonable name.
# It should store the data necessary to create a BikeStation object (Assignment 1)
# Instead of reading raw  JSON data from the web as done in the example, your program will connect to your MongoDB database and collection created in Assignment 2,
# Then you can loop through all of the documents in your bike_station collection and extract the relevant data from the dictionary object for each bike station and insert it into the database table.
# Secure Coding
# It should extract the data from the MongoDB data and store it individual variables for each piece of data you are writing to the database.
# It should cast numeric variables as int() or float() and break out of the data processing loop if the data is not of the correct format.
# It should convert ISO formatted date to a date time to validate it as well BUT, since you cannot store Dates=Time data in SQLite, you should store the data in the database as either an ISO formatted date or as a numeric time stamp.
# It should use a parameterized query to minimize the opportunity for SQLInjection.
# The Final Product
# When you are done, you will have a nicely indexed version of the bike station data in index.sqlite.
# This is the file to use to do data analysis (project 4)*/