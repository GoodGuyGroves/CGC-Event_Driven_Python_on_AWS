"""CGC ETL Lambda"""
import os
import logging
from etl import ETLHandler
import utils
import boto3


def main(event, context):
    """Lambda entry point"""

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info(event)
    logger.info(context)

    sns_topic_arn = os.environ["SNS_TOPIC_ARN"]
    sns = boto3.client("sns")

    try:
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
        logger.info("New data: %s", new_data)
        etl.db_store(new_data)
    except Exception as e:
        # Doing a general catch because I want all errors to be pushed to SNS
        sns.publish(
            TopicArn=sns_topic_arn,
            Message=(
                f"There was an error in function {context.function_name}"
                f"Please see log {context.log_group_name} for more info."
                f"Error: {e}"
            ),
        )
