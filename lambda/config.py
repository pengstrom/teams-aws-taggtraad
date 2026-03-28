from enum import StrEnum
import json
import os

from aws_lambda_powertools import Logger


RESULT_NO_ACTION = {"result": "ok", "notify": False}
RESULT_NOTIFIED = {"result": "ok", "notify": True}


logger = Logger()


class ConfigKey(StrEnum):
    REQUIRED_KEYS_KEY = "REQUIRED_KEYS"
    TEAMS_WEBHOOK_URL_KEY = "TEAMS_WEBHOOK_URL"
    ERROR_WEBHOOK_URL_KEY = "ERROR_WEBHOOK_URL"


class AppConfig:
    webhook_url: str
    error_webhook_url: str
    req_keys: list[str]

    def __init__(self):
        req_keys_s = os.environ.get(ConfigKey.REQUIRED_KEYS_KEY)
        logger.debug(req_keys_s)
        if req_keys_s is None:
            raise Exception(
                f"Could not find {ConfigKey.REQUIRED_KEYS_KEY} in env! Got: '{req_keys_s}'"
            )
        try:
            req_keys = json.loads(req_keys_s)
        except Exception as err:
            logger.error(f"Could not JSON parse: '{req_keys_s}'!")
            raise err
        if type(req_keys) is not list:
            raise Exception(
                f"Could not parse {ConfigKey.REQUIRED_KEYS_KEY} into list! Got: '{req_keys}'"
            )
        for k in req_keys:
            if type(k) is not str:
                raise Exception(
                    f"Could not parse {ConfigKey.REQUIRED_KEYS_KEY} into list of strings! Got: '{req_keys}'"
                )
        self.req_keys = req_keys

        error_webhook_url = os.environ.get(ConfigKey.ERROR_WEBHOOK_URL_KEY)
        logger.debug(error_webhook_url)
        if error_webhook_url is None:
            raise Exception(
                f"Could not find {ConfigKey.ERROR_WEBHOOK_URL_KEY} in env! Got: '{error_webhook_url}'"
            )
        error_webhook_url = error_webhook_url.strip()
        if error_webhook_url == "":
            raise Exception(
                f"Could not parse {ConfigKey.ERROR_WEBHOOK_URL_KEY} into non-empty string! Got: '{error_webhook_url}'"
            )
        self.error_webhook_url = error_webhook_url

        webhook_url = os.environ.get(ConfigKey.TEAMS_WEBHOOK_URL_KEY)
        logger.debug(webhook_url)
        if webhook_url is None:
            raise Exception(
                f"Could not find {ConfigKey.TEAMS_WEBHOOK_URL_KEY} in env! Got: '{webhook_url}'"
            )
        webhook_url = webhook_url.strip()
        if webhook_url == "":
            raise Exception(
                f"Could not parse {ConfigKey.TEAMS_WEBHOOK_URL_KEY} into non-empty string! Got: '{webhook_url}'"
            )
        self.webhook_url = webhook_url


config = AppConfig()
