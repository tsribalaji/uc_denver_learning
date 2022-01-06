import json
import pymongo
import urllib.request, urllib.parse, urllib.error
from datetime import datetime


class APIDataDownloader():
    """
    This Class get the data from URL and for the specified IDs.
    Constructor will take URL, bike station IDs, data download limit, order by.
    """

    def __init__(self, config):
        self.url = config['url']
        self.bike_station_ids = config['bike_station_ids']
        self.order_by = config['order_by']
        self.data_limit = config['data_limit']
        self.data = []

    def get_download_url(self, id):
        param = dict()
        param["id"] = id
        param["$order"] = self.order_by
        param["$limit"] = self.data_limit
        param = urllib.parse.urlencode(param)
        return self.url + param

    def get_document_from_url(self, url):
        """
        Using URL lib data will be downloaded.
        :param url: URL with parameters
        :return: return response
        """
        print("Getting Data from URL", url)
        document = urllib.request.urlopen(url)
        # get all of the text from the document
        return document

    def validate_document(self, document):
        """
        validate response whether it is success or not
        :param document: document response from request
        :return: Success or Error
        """
        if document.getcode() != 200:
            return "Error code=", document.getcode()
        return "Success"

    def get_data_for_id(self, id):
        """
        Read the response text and convert it to json result
        :param id: Bike Station ID
        :return: JSON result
        """
        url = self.get_download_url(id)
        document = self.get_document_from_url(url)
        validation = self.validate_document(document)
        if validation == 'Success':
            response_text = document.read().decode()
            json_result = json.loads(response_text)
            return json_result
        else:
            print(validation, url)
            return None

class DBBase():
    """
    Database Base class, which initiate the connection for specified connection string
    Constructor: take config with connection string, user ID and password
    """

    def __init__(self, config):
        self.connection_string = config['connection_string']
        self.user = config['user']
        self.password = config['password']
        self.client = self.__connect()

    def __connect(self):
        """
        Create the connection with mongo Atlas server
        :return: MongoClient object
        """
        client = pymongo.MongoClient(self.connection_string.format(self.user, self.password))
        db = client.test
        print(db)
        return client

    def __create_db(self, name):
        """
        Check whether db exist in mongo server
        :param name: Database Name
        :return: Database object
        """
        if not self.__is_db_exist(name):
            result = self.client[name]
            return result

    def __is_db_exist(self, name):
        """
        Get all the database from the server and check name in databse list
        :param name: database name
        :return: Boolean - True or False
        """
        db_list = self.client.list_database_names()
        if name in db_list:
            return True
        else:
            return False

    def get_db(self, name):
        """
        Get the database object from the server.
        :param name: Database name
        :return: Database object
        """
        if self.__is_db_exist(name):
            return self.client[name]
        else:
            db = self.__create_db(name)
            return db


class BikeStationDBClient(DBBase):
    def __init__(self, config):
        super().__init__(config)
        self.db = self.get_db("BikeStation")

    def __check_collection_exist(self, name):
        """
        check the collection exist in database or not
        :param name: collection name
        :return: Boolean true or false
        """
        collections = self.db.list_collection_names()
        if name in collections:
            return True
        else:
            return False

    def get_collection(self, name):
        """
        get the collection from the database
        :param name: collection name
        :return: collection object
        """
        if self.__check_collection_exist(name):
            return self.db[name]
        else:
            return self.db[name]

    def insert_many(self, collection_name, data):
        """
        Stores the list of documents to collection
        :param collection_name: Mongo Document/Collection Name
        :param data: list object
        """
        collection = self.get_collection(collection_name)
        if collection is not None:
            old_count = collection.count()
            collection.insert_many(data)
            new_count = collection.count()
            print(new_count - old_count, "- Records Updated")
        else:
            print('Collection Not Found in database, Please create the collection and insert')

    def execute_query(self, collection_name, query):
        """
        Execute the query/filter to get the data from the collection
        :param collection_name: Mongo Document/Collection Name
        :param query: filter
        :return: query result - Cursor
        """
        collection = self.get_collection(collection_name)
        docs = collection.find(query)
        return docs


class BikeStationDataDownloader():
    def __init__(self, db_config, data_config):
        self.bike_station_ids = data_config['bike_station_ids']
        self.data_downloader = APIDataDownloader(data_config)
        self.bike_station_db = BikeStationDBClient(db_config)

    def get_bike_station_data(self):
        """
        Get the response from the specified URL and IDs and store it to mongo DB
        """
        try:
            for id in self.bike_station_ids:
                print("Bike Station id - ", id)
                data = self.data_downloader.get_data_for_id(id)
                if data is not None:
                    self.bike_station_db.insert_many('BikeStationData', data)
                if len(data) < 1000:
                    print("Data downloaded from the API is less than 1000")
        except:
            print('Unable to download the data, Please try again later')

    def get_total_records(self):
        query = {"id": {"$in": self.bike_station_ids}}
        stored_data = self.bike_station_db.execute_query('BikeStationData', query)
        print("Total Records in Collection for given Ids - ", stored_data.count())

    def validate_data(self):
        collection = self.bike_station_db.get_collection('BikeStationData')
        result = collection.aggregate([
            {"$group": {"_id": {"id": "$id"}, "total_count": {"$sum": 1},
                        "latest_timestamp": {"$max": "$timestamp"}}}])

        for x in result:
            print("Bike Station " + x["_id"]["id"] + " Has " + str(x["total_count"]))
            timestamp = datetime.fromisoformat(x["latest_timestamp"])
            print("Latest Record Timestamp", timestamp.strftime("%a %b %d %X %Y"))

    def download(self):
        self.get_bike_station_data()
        print("\n==============Data Validation==========\n")
        self.get_total_records()
        self.validate_data()


def main():
    data_config = {'url': 'https://data.cityofchicago.org/resource/eq45-8inv.json?',
                   'bike_station_ids': ["157", "220", "324", "329", "340"], 'order_by': 'timestamp DESC',
                   'data_limit': 5000}

    db_config = dict(
        connection_string='mongodb+srv://{0}:{1}@cluster0.s5bx2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority',
        user='m001-student', password='m001-mongodb-basics')

    downloader = BikeStationDataDownloader(db_config, data_config)
    downloader.download()


if __name__ == "__main__":
    main()
