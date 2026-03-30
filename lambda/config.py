from enum import StrEnum
import os
import dotenv
from model import Case
from teams import Webhook


RESULT_NO_ACTION = {"result": "ok", "notify": False}
RESULT_NOTIFIED = {"result": "ok", "notify": True}




class ConfigKey(StrEnum):
    NOTIFY_WEBHOOK_URL_KEY = "NOTIFY_WEBHOOK_URL"
    ERROR_WEBHOOK_URL_KEY = "ERROR_WEBHOOK_URL"
    REQUIRED_KEYS_KEY = "REQUIRED_KEYS"
    KEY_CASE = "KEY_CASE"
    VALUE_CASE = "VALUE_CASE"


def _env_str(k: str) -> str:
    value = os.environ.get(k)
    if value is None:
        raise Exception(
            f"Could not find {k} in env! Got: '{value}'"
        )
    value = value.strip()
    if value == "":
        raise Exception(
            f"Could not parse env var {k} into non-empty string! Got: '{value}'"
        )
    return value

def _env_strs(k: str) -> list[str]:
    value = os.environ.get(k)
    if value is None:
        raise Exception(
            f"Could not find {k} in env! Got: '{value}'"
        )
    
    values = value.split()
    return values

def _env_case(k: str) -> Case:
    value = _env_str(k).lower()
    if value in ["lower", "lowercase"]:
        return Case.LOWER
    if value in ["upper", "uppercase"]:
        return Case.UPPER
    if value in ["capital", "capitalize", "capitalized"]:
        return Case.CAPILATIZE
    
    raise Exception(f"Env var {k} is not a valid case! Expected one of {[Case.LOWER, Case.UPPER, Case.CAPILATIZE]}, got '{value}'")


class AppConfig:
    notify_webhook_url: str
    error_webhook_url: str
    req_keys: list[str]
    key_case: Case
    value_case: Case

    notify_client: Webhook
    error_client: Webhook

    def __init__(self):
        dotenv.load_dotenv()
        self.req_keys = _env_strs(ConfigKey.REQUIRED_KEYS_KEY)
        self.key_case = _env_case(ConfigKey.KEY_CASE)
        self.value_case = _env_case(ConfigKey.VALUE_CASE)

        self.notify_webhook_url = _env_str(ConfigKey.NOTIFY_WEBHOOK_URL_KEY)
        self.error_webhook_url = _env_str(ConfigKey.ERROR_WEBHOOK_URL_KEY)

        self.notify_client = Webhook(self.notify_webhook_url)
        self.error_client = Webhook(self.error_webhook_url)


cfg = AppConfig()
