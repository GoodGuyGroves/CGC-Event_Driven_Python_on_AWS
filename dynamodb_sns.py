"""Emails data about DynamoDB updated roles"""
import logging


def alert(event, context):
    """Sends the alert"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info(event)
    logger.info(context)
