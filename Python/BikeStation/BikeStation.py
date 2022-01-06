import os
import re
from datetime import datetime
from downloader import DownloadData


class Point:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    @property
    def latitude(self):
        return self.latitude

    @latitude.setter
    def latitude(self, x):
        self.__latitude = x

    @property
    def longitude(self):
        return self.longitude

    @longitude.setter
    def longitude(self, x):
        self.__longitude = x

    def coordinates(self):
        return [self.longitude, self.latitude]


class BikeStation:
    def __init__(self, bike_station):
        self.id = bike_station['id']
        self.timestamp = bike_station['timestamp']
        self.station_name = bike_station['station_name']
        self.total_docks = bike_station['total_docks']
        self.docks_in_service = bike_station['docks_in_service']
        self.available_docks = bike_station['available_docks']
        self.status = bike_station['status']
        self.record = bike_station['record']
        self.location = self.set_location(bike_station['latitude'], bike_station['longitude'])

    @property
    def record(self):
        return self.record

    @record.setter
    def record(self, x):
        x = int(x)
        if x == 0:
            return "ID cannot be zero"
        self.__record = x

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, x):
        x = int(x)
        if x == 0:
            return "ID cannot be zero"
        self.__id = x

    @property
    def timestamp(self):
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, x):
        dt = datetime.fromisoformat(x)
        self.__timestamp = dt

    @property
    def station_name(self):
        return self.__station_name

    @station_name.setter
    def station_name(self, x):
        if x is None or x == "":
            return "Station Name cannot be empty"
        self.__station_name = x

    @property
    def total_docks(self):
        return self.__total_docks

    @total_docks.setter
    def total_docks(self, x):
        x = int(x)
        self.__total_docks = x

    @property
    def available_docks(self):
        return self.__available_docks

    @available_docks.setter
    def available_docks(self, x):
        x = int(x)
        if x == 0:
            return "Total Docks cannot be Zero"
        self.__available_docks = x

    @property
    def docks_in_service(self):
        return self.__docks_in_service

    @docks_in_service.setter
    def docks_in_service(self, x):
        self.__docks_in_service = x

    @staticmethod
    def set_location(latitude, longitude):
        return Point(latitude, longitude)

    def get_percent_full(self):
        """
        Calculates the percentage of available bikes in the bike station.
        :return: int: percent value
        """
        available_bikes = self.get_total_bikes_available()
        percent_full = (available_bikes / self.docks_in_service) * 100
        return round(percent_full)

    def get_total_bikes_available(self):
        """
        Calculates available number of bikes from the total
        docks and available docks
        :return int: available number of bikes
        """
        available_bikes = self.total_docks - self.available_docks
        return available_bikes

    def __str__(self):
        timestamp_str = d = self.timestamp.strftime("%a %b %d %X %Y")
        text_to_print = '{0} had {1} bikes on {2}' \
            .format(self.station_name,
                    str(self.get_total_bikes_available()),
                    timestamp_str)
        return text_to_print


class BikeStationSummary:
    def __init__(self, filename, bike_station_IDs=None):
        """
        Input will be file and bike station IDs to read from the file
        Bike Station Id is optional, if it is None all the bike stations will be retrieved.
        :type bike_station_Id: object
        """
        self.bike_stations_filter = bike_station_IDs
        self.filename = filename
        self.bike_stations = []

    def read_file(self):
        """
        Open the given file and return the lines
        :return List[str]: all the lines from the file
        """
        lines = []
        try:
            if self.filename is not None:
                file = open(self.filename)
                lines = file.readlines()
                file.close()
        except:
            print('Error:  Unable to open the file')
            return None
        return lines

    def extract_values_from_line(self, line):
        """
        This method will extract value from the line
        Co-Ordinates in the location will ignored from
        the input line since we have longitude and latitude.
        :param: line: Single line from the input file
        :return: Dict[str, str] : All the values from the input line like Id, timestamp etc and its value
        """
        lineValues = {}
        values = line.split(',')
        for value in values:
            if "location" in value or "coordinates" in value or ":" not in value:
                continue
            else:
                """
                Here, Instead the getting the value by its index, I converted it key value pair
                which help me avoid code re-write when there is a change in the value location. 
                """
                keyValuePair = value.strip().split(': ')
                key = re.sub('[\[{"}\]]', '', keyValuePair[0])
                value = re.sub('[\[{"}\]]', '', keyValuePair[1])
                lineValues[key] = value
        return lineValues

    def extract_data_from_file(self, lines):
        """
        Extract the bike stations information lines which are assigned to me.
        :param lines: List of the all lines extracted from the text file.
        """
        for line in lines:
            # this condition will execute when there is no filter and also filtering the given IDs.
            if self.bike_stations_filter is None or any(
                    ('id": "' + x + '"') in line for x in self.bike_stations_filter):
                station = BikeStation(self.extract_values_from_line(line))
                self.bike_stations.append(station)

    def print_summary(self):
        """
        This Function will print the available bikes and docks count for the 5 stations.
        :type: BikeStations: List of BikeStation
        """
        total_bikes = 0
        total_docks = 0
        bike_station_ID = []
        for bike_station in self.bike_stations:
            print(bike_station)  # Overridden __str__ method will be invoked to print a bike station's summary.
            total_bikes = total_bikes + bike_station.get_total_bikes_available()
            total_docks = total_docks + bike_station.available_docks
            bike_station_ID.append(str(bike_station.id))
        summary = "Stations: [{0}] Bikes Available {1} Docks Available {2}" \
            .format(', '.join(bike_station_ID), str(total_bikes), str(total_docks))
        print(summary)







def get_filename():
    """
    Prompt the user to enter the filename and check if the file
    is exist in the given path or not
    :return string: file name
    """
    fileName = input("Please enter data file path\n")
    if fileName is None or not os.path.exists(fileName):
        print('Please enter the valid filename')
    else:
        return fileName


# def main():
#     """
#     Main method, which get inputs from the user and read the file to extract
#     the bike station information, to get information like available bike and dock count.
#     :return: None
#     """
#     bike_station_IDs = ["157", "220", "324", "329", "340"]
#     filename = get_filename()
#     summarizer = BikeStationSummary(filename, bike_station_IDs)
#     lines = summarizer.read_file()
#     if lines is not None:
#         summarizer.extract_data_from_file(lines)
#         summarizer.print_summary()

def main():
    config = {'url': 'https://data.cityofchicago.org/resource/eq45-8inv.json?',
              'bike_station_ids': ["157", "220", "324", "329", "340"], 'order_by': 'timestamp DESC', 'data_limit': 5} #
    downloader = DownloadData(config)
    data = downloader.get_data_for_bike_stations()
    print(data)


if __name__ == "__main__":
    main()
