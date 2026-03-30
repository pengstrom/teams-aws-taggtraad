from aws_lambda_powertools.utilities.typing import LambdaContext
from logger import logger
from config import *
from event.dispatch import dispatch
from event.envelope import EventBridgeEvent
from business import send_notification
from error import handle_unexpected


@logger.inject_lambda_context(log_event=logger.log_level <= 20)  # DEBUG = 10, INFO = 20
def handler(original: dict, ctx: LambdaContext):
    try:
        event = EventBridgeEvent.model_validate(original, by_alias=True, from_attributes=True)
        resource_report = dispatch(event)
        if resource_report.reports:
            send_notification(original, event, resource_report)
            return RESULT_NOTIFIED
        else:
            return RESULT_NO_ACTION
    except Exception as e:
        handle_unexpected(e, original, ctx)
        raise
