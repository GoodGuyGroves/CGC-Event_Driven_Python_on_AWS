"""Loads Covid-19 data from CSV files"""
import pandas as pd
import csvutils
import boto3
from dynamodb_json import json_util as json

import matplotlib.pyplot as plt
import seaborn as sns
import mpld3


class ETLHandler:
    """Takes a Pandas DataFrame, compares it to a database and updates the data"""

    def __init__(self):
        self.table = self.db_connect()

    def db_connect(self):
        """Connects to the DynamoDB Table"""
        dynamodb = boto3.resource(
            "dynamodb",
            region_name="af-south-1",
            aws_access_key_id="AKIAZJ54PQLL2U7BNTFG",
            aws_secret_access_key="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",
        )
        return dynamodb.Table("covid-stats")

    def db_store(self, df: pd.DataFrame):
        """Stores Pandas DataFrame into DynamoDB"""
        json_data = df.T.to_dict().values()
        for entry in json_data:
            try:
                entry["recovered"] = int(entry["recovered"])
            except ValueError:
                entry["recovered"] = 0
            print(f"Storing: {entry}")
            self.table.put_item(Item=entry)

    def db_load(self) -> pd.DataFrame:
        """Loads data from DynamoDB into Pandas DataFrame"""
        response = self.table.scan()
        data = response["Items"]
        while "LastEvaluatedKey" in response:
            response = self.table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
            data.extend(response["Items"])
        return pd.DataFrame(json.loads(data))

    def data_diff(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compares a DataFrame with data already stored in the DB"""
        old_df = self.db_load()
        try:
            # If there is already data in DynamoDB, this diff will work
            diff_df = csvutils.find_new(old_df, df)
        except AttributeError:
            # If there is no data in DynamoDB yet, an AttributeError will be raised
            # Here we create a blank DataFrame to diff against
            df_columns = ["date", "cases", "deaths", "recovered"]
            old_df = pd.DataFrame(columns=df_columns)
            try:
                # We now try the diff again, this nested try/except block follows
                # EAFP: Easier to ask for forgiveness than permission
                diff_df = csvutils.find_new(old_df, df)
            except Exception as e:
                # I don't yet know what other possible issues could arise so general catch for now
                print(e)
        return diff_df

    @staticmethod
    def data_vis(df: pd.DataFrame, start_date, end_date):
        """Visualise your data"""

        sns.set_style("whitegrid")
        plt.figure(figsize=(16, 9))

        df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

        sns.lineplot(x="date", y="value", hue="variable", data=pd.melt(df, ["date"]))

        sns.despine()
        plt.show()

        plt.savefig("foo.png")

if __name__ == "__main__":
    # Load two CSV's
    nyt = csvutils.load_csv(
        "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"
    )
    jh = csvutils.load_csv(
        "https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv"
    )
    # Operate on the two CSV's to merge their data
    jh = csvutils.filter_criteria(jh, "Country/Region", "US")
    my_df = csvutils.merge_df(nyt, jh, ["Date", "Recovered"], "date", "Date")
    my_df = csvutils.remove_column(my_df, "Date")
    my_df = csvutils.lowercase_columns(my_df)

    etl = ETLHandler()
    etl.data_vis(my_df, "2020-02-21", "2020-03-05")

    # etl = ETLHandler()
    # new_data = etl.data_diff(my_df)
    # etl.db_store(new_data)

    # Ghetto test
    # new_data = new_data.append(pd.DataFrame({"date":'2020-09-14',"cases": [1],"deaths": [2], "recovered": [3]}))
    # print(new_data)
