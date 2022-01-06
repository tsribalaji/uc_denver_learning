import sqlite3
from datetime import datetime
import pymongo

class MongoClient:
    def __init__(self, config):
        self.connection_string = config['connection_string']
        self.user = config['user']
        self.password = config['password']
        self.db_name = config['database']
        self.client = self.__connect()

    def __connect(self):
        """
        Create the connection with mongo Atlas server
        :return: MongoClient object
        """
        client = pymongo.MongoClient(self.connection_string.format(self.user, self.password))
        db = client.test
        print("Mongo Connection -- ",db)
        return client

    def get_collection(self, name):
        """
        get the collection from the database
        :param name: collection name
        :return: collection object
        """
        print("Downloading data from Mongo Atlas")
        db = self.client[self.db_name]
        doc = db[name]
        if doc is not None:
            return doc
        else:
            return "collection not found in Mongo Atlas Server"


class SQLClient:
    def __init__(self):
        self.__conn = sqlite3.connect('index.sqlite')
        self.__cur = self.__conn.cursor()
        self.clean_create_DB()

    def clean_create_DB(self):
        """
        Deletes the existing table and create the new table for location and bike station.
        :return:
        """
        self.__cur.execute('DROP TABLE IF EXISTS locations')
        self.__cur.execute('DROP TABLE IF EXISTS bike_stations')

        self.__cur.execute('CREATE TABLE locations (\n'
                           'location_id INTEGER NOT NULL, \n'
                           'latitude FLOAT, \n'
                           'longitude FLOAT, \n'  
                           'PRIMARY KEY("location_id")\n'                           
                           ');')

        self.__cur.execute('CREATE TABLE bike_stations (\n'
                           '	"record"	INTEGER  NOT NULL,\n'
                           '	"stationId"	INTEGER,\n'
                           '	"station_name"	TEXT,\n'
                           '	"total_docks"	INTEGER,\n'
                           '	"timestamp"	TEXT,\n'
                           '	"available_docks"	INTEGER,\n'
                           '	"docks_in_service"	INTEGER,\n'
                           '    "point_id" INTEGER, \n'       
                           '	PRIMARY KEY("record")\n'
                           '    FOREIGN KEY ("point_id") REFERENCES locations (location_id) \n'
                           ');')

    def get_location_id(self, query):
        """
        Checks whether the location details are already there in the table, if not new record will be inserted.
        :param query:
        :return:
        """
        try:
            location_id = None
            self.__cur.execute('''SELECT location_id FROM locations WHERE longitude=? and latitude=?''', query)
            location_id = self.__cur.fetchone()
            if location_id is None:  # insert location if not already present in locations table
                self.__cur.execute('''INSERT INTO locations(longitude,latitude)
                VALUES(?,?)''', (query[0], query[1]))
                return self.__cur.lastrowid
            else:
                return location_id[0]
        except Exception as ex:
            raise ex

    def insert(self, data_query):
        try:
            self.__cur.execute('''INSERT INTO bike_stations (stationId, station_name, total_docks, timestamp, 
                               available_docks, docks_in_service, record, point_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', data_query)
        except Exception as ex:
            raise ex

    def get_row_inserted_count(self):
        cursor = self.__cur.execute('select * from bike_stations ;')
        return len(cursor.fetchall())

    def commit_changes(self):
        self.__conn.commit()


class ModelData:
    def __init__(self, mongo_config):
        self.collection_name = ""
        mongo_config = dict(
            connection_string='mongodb+srv://{0}:{1}@cluster0.s5bx2.mongodb.net/myFirstDatabase?retryWrites=true&w'
                              '=majority',
            user='m001-student', password='m001-mongodb-basics', database="BikeStation")
        self.mongo_client = MongoClient(mongo_config)
        self.sql_client = SQLClient()

    def download_data_from_mongo(self):
        """
        Get the stored data from the mongo Atlas server
        :return: Collection
        """
        return self.mongo_client.get_collection('BikeStationData')

    def validate_data(self, data):
        """
        validate the give data, by converting to its actual format from string.
        :param data: string data from mongo
        :return: True or False
        """
        try:
            timestamp = datetime.fromisoformat(data['timestamp']).strftime("%d-%b-%Y (%H:%M:%S.%f)")
        except Exception as ex:
            print('Invalid date format, Unable to insert data in SQLite', str(ex))
            return False

        try:
            id = int(data['id'])
            total_docks = int(data['total_docks'])
            available_docks = int(data['available_docks'])
            docks_in_service = int(data['docks_in_service'])
            record = int(data['record'])
            latitude = float(data['latitude'])
            longitude = float(data['longitude'])
        except Exception as ex:
            print('Error while converting string to int, Unable to insert data in SQLite', str(ex))
            return False
        return True

    def save_data_to_sqlite(self):
        """
        Get the data from the Mongo database Atlas server and stores into local sqlite file
        """
        data = self.download_data_from_mongo()

        cur = data.find()
        print("Inserting data into sqlite")

        count = 0
        for data in cur:
            if self.validate_data(data):
                loc_query = (float(data['latitude']), float(data['longitude']))
                location_id = self.sql_client.get_location_id(loc_query)
                data_query = (int(data['id']), data['station_name'], int(data['total_docks']), data['timestamp'],
                         int(data['available_docks']), int(data['docks_in_service']), int(data['record']), location_id)
                self.sql_client.insert(data_query)
            else:
                break
            # increment count
            count = count + 1
            # commit the insert statemnt(s) for every 100 records so do not slow program down
            if count % 100 == 0:
                self.sql_client.commit_changes()
                print(f"\nRows inserted to SQLite db so far - {self.sql_client.get_row_inserted_count()}")
                print(f"Updated bike station records till {data['timestamp']} for bike station {data['station_name']}")

        print(f"\nTotal rows inserted to SQLite db - {self.sql_client.get_row_inserted_count()}")

def main():
    db_config = dict(
        connection_string='mongodb+srv://{0}:{1}@cluster0.s5bx2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority',
        user='m001-student', password='m001-mongodb-basics')

    downloader = ModelData(db_config)
    downloader.save_data_to_sqlite()


if __name__ == "__main__":
    main()
