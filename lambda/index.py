# from aws_lambda_powertools.utilities.typing import LambdaContext
# from aws_lambda_powertools.utilities.data_classes import EventBridgeEvent
import os
from aws.event_bridge import *
from business import Tagger, TagConfig, get_tags, report_tag_errors
from config import AppConfig
from business.tag import Case
from error import report_error
from aws_lambda_powertools.logging import Logger

logger = Logger()


@logger.inject_lambda_context(log_event=True)
def handler(ev: dict, ctx):

    cfg = None
    try:
        cfg = AppConfig()

        api_event = AWSAPICallViaCloudTrail.model_validate(ev.get("detail"))
        print("api_event")
        print(api_event)

        tagger = Tagger(TagConfig(cfg.req_keys, Case.CAPILATIZE, Case.LOWER))
        tags = get_tags(api_event)
        errors = tagger.validate(tags)
        if len(errors) > 0:
            return report_tag_errors(cfg.webhook_url, api_event, errors)
        else:
            return {"status": "ok"}
    except Exception as err:
        print("Event:")
        print(ev)
        print("Context:")
        print(ctx)

        print("REQUIRED_TAGS:")
        print(os.environ.get("REQUIRED_TAGS"))
        print("Could not validate!")
        print(err)
        print("TEAMS_WEBHOOK_URL:")
        print(os.environ.get("TEAMS_WEBHOOK_URL"))

        if cfg:
            report_error(cfg, err)

        return {"status": "error", "err": str(err)}
