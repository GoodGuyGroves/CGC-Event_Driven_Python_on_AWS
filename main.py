"""Loads Covid-19 data from CSV files"""
import pandas as pd
import numpy as np

# Use for testing
# new_df = df.append(pd.DataFrame({"date":'2020-09-14',"cases": [1],"deaths": [2]}))

class CSVParse():
    """Takes in a url of a CSV and parses it"""

    def __init__(self, csv_url):
        self.csv_url = csv_url
        self.df = None
        self.load_csv()

    def load_csv(self):
        """Loads a CSV from a URL into a Pandas DataFrame"""
        self.df = pd.read_csv(self.csv_url, index_col=None)

    def find_new(self, cur_data: pd.DataFrame, new_data: pd.DataFrame) -> pd.DataFrame:
        """Takes in two Pandas DataFrames, finds which rows exist only in the new
        dataframe and returns them only as a new DataFrame"""
        return new_data[np.equal(new_data.date.isin(cur_data.date), False)]

    def convert_date(self):
        """Converts all date strings into datetime objects"""
        self.df['date'] = pd.to_datetime(self.df['date'], format='%Y-%m-%d')

if __name__ == '__main__':
    my_csv = CSVParse(
        'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
        )
    # my_csv = CSVParse(
    #     'https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv'
    #     )
    print(my_csv.df)