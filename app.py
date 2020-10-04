"""CGC ETL Lambda"""
import logging
from etl import ETLHandler
import utils

def main(event, context):
    """Lambda entry point"""

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info(event)
    logger.info(context)

    # Load two CSV's
    nyt = utils.load_csv(
        "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"
    )
    jh = utils.load_csv(
        "https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv"
    )
    # Operate on the two CSV's to merge their data
    jh = utils.filter_criteria(jh, "Country/Region", "US")
    my_df = utils.merge_df(nyt, jh, ["Date", "Recovered"], "date", "Date")
    my_df = utils.remove_column(my_df, "Date")
    my_df = utils.lowercase_columns(my_df)

    etl = ETLHandler()
    new_data = etl.data_diff(my_df)
    print(new_data)
    etl.db_store(new_data)

    # Ghetto test
    # new_data = new_data.append(pd.DataFrame({"date":'2020-09-14',"cases": [1],"deaths": [2], "recovered": [3]}))
    # print(new_data)
