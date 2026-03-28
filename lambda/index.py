import os

# from aws_lambda_powertools.logging import Logger
from config import *
from event.dispatch import dispatch
from event.envelope import EventBridgeEvent
from business import send_notification
from error import handle_unexpected


@logger.inject_lambda_context(log_event=logger.log_level <= 20)  # DEBUG = 10, INFO = 20
def handler(ev: dict, ctx):
    try:
        event = EventBridgeEvent.model_validate(ev, by_alias=True)
        resource_report = dispatch(event)
        if resource_report.reports:
            send_notification(event, resource_report)
            return RESULT_NOTIFIED
        else:
            return RESULT_NO_ACTION
    except Exception as e:
        handle_unexpected(e, ev)
        raise
