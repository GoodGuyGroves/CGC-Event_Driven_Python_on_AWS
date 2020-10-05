"""Loads Covid-19 data from CSV files"""
import logging
import pandas as pd
import utils
import boto3
from dynamodb_json import json_util as json


class ETLHandler:
    """Takes a Pandas DataFrame, compares it to a database and updates the data"""

    def __init__(self):
        self.table = self.db_connect()
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

    @staticmethod
    def db_connect():
        """Connects to the DynamoDB Table"""
        dynamodb = boto3.resource("dynamodb", region_name="af-south-1")
        return dynamodb.Table("covid-stats")

    def db_store(self, df: pd.DataFrame):
        """Stores Pandas DataFrame into DynamoDB"""
        json_data = df.T.to_dict().values()
        for entry in json_data:
            try:
                entry["recovered"] = int(entry["recovered"])
            except ValueError:
                entry["recovered"] = 0
            self.logger.info("Storing: %s", entry)
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
            diff_df = utils.find_new(old_df, df)
        except AttributeError:
            # If there is no data in DynamoDB yet, an AttributeError will be raised
            # Here we create a blank DataFrame to diff against
            df_columns = ["date", "cases", "deaths", "recovered"]
            old_df = pd.DataFrame(columns=df_columns)
            try:
                # We now try the diff again, this nested try/except block follows
                # EAFP: Easier to ask for forgiveness than permission
                diff_df = utils.find_new(old_df, df)
            except Exception as e:
                # I don't yet know what other possible issues could arise so general catch for now
                self.logger.info(e)
        return diff_df
