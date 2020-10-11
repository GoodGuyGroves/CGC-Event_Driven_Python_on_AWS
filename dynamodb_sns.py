"""Emails data about DynamoDB updated roles"""
import os
import logging
import boto3


def alert(event, context):
    """Sends the alert"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info(event)
    logger.info(context)

    sns_topic_arn = os.environ["SNS_TOPIC_ARN"]
    sns = boto3.client("sns")

    message = ""

    func_name = context.function_name
    logger.info(func_name)
    trigger_arn = context.invoked_function_arn
    logger.info(trigger_arn)
    log_group_name = context.log_group_name
    logger.info(log_group_name)
    log_stream_name = context.log_stream_name
    logger.info(log_stream_name)

    message += (
        f"Function: {func_name}\n"
        f"Trigger: {trigger_arn}\n"
        f"Log Group: {log_group_name}\n"
        f"Log Stream: {log_stream_name}\n"
        f"\nNew rows added:\n"
    )

    new_rows = []
    for record in event["Records"]:
        if record["eventName"] == "INSERT":
            if "NewImage" in record["dynamodb"]:
                new_rows.append(record["dynamodb"]["NewImage"])

    new_rows_str = [str(x) for x in new_rows]
    message += "\n".join(new_rows_str)

    sns.publish(TopicArn=sns_topic_arn, Message=message)
    return message
