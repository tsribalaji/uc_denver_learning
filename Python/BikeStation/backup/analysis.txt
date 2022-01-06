import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import bike_station


class SQLClient:
    def __init__(self):
        self.__conn = sqlite3.connect('index.sqlite')
        self.__conn.text_factory = str
        self.__cur = self.__conn.cursor()

    def get_bike_stations(self):
        """
        Gets the bike station records for this connection instance
        :return: list of Bike_station object
        """
        try:
            result = None
            self.__cur.execute('''SELECT record, stationId, station_name, total_docks, 
                timestamp, available_docks, docks_in_service FROM bike_stations''')
            result = self.__cur.fetchall()
            # Create a list of BikeStation objects using the BikeStation class created in the OOP assignment
            bike_stations_list = []

            for bike_station_data in result:
                bike_stations_list.append(bike_station.BikeStation(bike_station_data))

            return bike_stations_list
        except Exception as ex:
            print("Unable to fetch data from SQLite")
            raise ex


class DataVisualization:
    def __init__(self, bike_station_list):
        # Converts list of class objects to DataFrame
        self.bike_df = pd.DataFrame([x.as_dict() for x in bike_station_list])
        self.process_bike_stations_data()

    def process_bike_stations_data(self):
        try:
            # Create additional columns as needed for further analysis
            self.bike_df['my_dates'] = pd.to_datetime(self.bike_df['timestamp'])
            self.bike_df['day_of_week'] = self.bike_df['my_dates'].dt.day_name()
            self.bike_df['date'] = self.bike_df['my_dates'].dt.date
            self.bike_df['available_bikes'] = self.bike_df['docks_in_service'] - self.bike_df['available_docks']

            # New columns are added for day of week, date and available_bikes
            print(f'Columns after data processing - \n{self.bike_df.columns}')
        except Exception as ex:
            print("Unable to process data frame")
            raise ex

    @staticmethod
    def save_show_plot(plot, plt_name):
        """ Shows plot in desired settings size and saves it
        Input: plot<maptplotlib.plt>, plt_name<str>
        """
        mng = plot.get_current_fig_manager()
        mng.window.showMaximized()

        plot.tight_layout()
        plot.xticks(rotation=40)

        plot.savefig(plt_name)
        plot.show()


    def print_stats(self):
        """
        Basic Stats: Avg of available_bikes and docks_in_service and min/max timestamp
        :return: None
        """
        try:
            table = pd.pivot_table(self.bike_df, values=['available_bikes', 'docks_in_service'], index=['id'],
                                   aggfunc={'available_bikes': np.mean,
                                            'docks_in_service': np.mean})
            print("\nBasic Stats: \n============\n", table)
        except Exception as ex:
            print("Unable to get/print stats from data")
            raise ex

    def plot_available_bikes(self):
        """
        Create a bar chart showing the average bikes and/or docks available by bike station
         Made directly from the Pandas DataFrame
         :return: None
         """

        bike_df_avg = self.bike_df.groupby(['id'])['available_docks'].mean()
        plt.title('Plot 1 - Bar chart showing Average docks available by bike station')
        plt.xlabel('Bike station id')
        plt.ylabel('Avg. docks available')
        bike_df_avg.plot.bar()

        # Save the figure and show the chart
        self.save_show_plot(plt, "Plot 1.png")

    def plot_available_bike_per_week(self):
        """
        # Create a bar chart showing the average bikes and/or docks available by day of the week (Monday,Tuesday ...).
        # Converting the timestamp to a datetime to create a new column in Data frame for day
        # associated with each reading
        :return: None
        """

        ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        bike_df_avg_by_day = self.bike_df.groupby(['day_of_week'])['available_docks'].mean().reindex(ordered_days)

        # In case of avg. docks by day by ID
        # bike_df_avg_by_day = pd.pivot_table(bike_df, values=['available_bikes'],
        #                       columns=['day_of_week'], index=['id'], aggfunc=np.mean)

        # bike_df_avg_by_day["available_bikes"].plot()
        bike_df_avg_by_day.plot.bar()

        plt.title('Plot 2 - Bar chart showing Average docks available by day_of_week')
        plt.xlabel('Day of week')
        plt.ylabel('Avg. docks available')

        # Save the figure and show the chart
        self.save_show_plot(plt, "Plot 2.png")

    def plot_available_bike_per_day(self):
        """
        Generates Line Plot chart showing Average bikes available available by time
        :return: None
        """
        bike_df_avg_by_day = pd.pivot_table(self.bike_df, values=['available_bikes'], columns=['id'], index=['date'],
                                            aggfunc=np.mean)

        bike_df_avg_by_day["available_bikes"].plot()  # default is 'line' - line plot
        plt.title('Plot 3 - Line Plot chart showing Average bikes available available by time')
        plt.xlabel('Time (in Date)')  # Scale used is dates
        plt.ylabel('Avg. bikes available')

        plt.tight_layout()
        plt.xticks(rotation=25)

        # Save the figure and show the chart
        self.save_show_plot(plt, "Plot 3.png")

    def plot_available_bikes_over_time(self):
        """
        Create a scatter plot of the number of bikes available or docks in service for each BikeStation over time.
        :return:None
        """
        # Used ax to set the legend of colors for each station
        fig, ax = plt.subplots()
        scatter = ax.scatter(self.bike_df['my_dates'], self.bike_df['available_bikes'], c=self.bike_df['id'],
                    label=self.bike_df['id'])
        legend1 = ax.legend(*scatter.legend_elements(),
                            loc="upper center", title="BikeStations - color map")
        ax.add_artist(legend1)

        # To set the limit of first and last point of date in x axis
        plt.xlim(np.min(self.bike_df['my_dates']), np.max(self.bike_df['my_dates']))

        plt.title('Plot 2 - Scatter Plot chart showing no. of bikes available over time')
        plt.xlabel('Time (in Date)')  # Scale used is dates
        plt.ylabel('No. of bikes available')

        # Save the figure and show the chart
        self.save_show_plot(plt, "Plot 2.png")


def main():
    try:
        # Step 1 - Extract data from Sqlite db
        sql_client = SQLClient()
        bike_stations = sql_client.get_bike_stations()

        analytics = DataVisualization(bike_stations)
        # Step 2: Statistical Analysis - calculating at least 2 statistics for each bike station
        analytics.print_stats()

        # Step 3: Generating plots using Pandas DataFrame,
        # from Pandas Series from the DataFrame for each column in the data frame,
        # and those series being used just like a list in matplotlib.pyplot.
        analytics.plot_available_bikes()
        # analytics.plot_available_bike_per_week()
        analytics.plot_available_bikes_over_time()
        analytics.plot_available_bike_per_day()
    except Exception as ex:
        print(f"Error: Unable to run analysis.py {str(ex)}")
        raise ex


if __name__ == "__main__":
    main()
