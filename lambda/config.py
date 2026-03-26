import json
import os


class AppConfig:
    webhook_url: str
    error_webhook_url: str
    req_keys: list[str]

    def __init__(self):
        req_keys_s = os.environ.get("REQUIRED_KEYS")
        if req_keys_s is None:
            raise Exception(f"Could not find REQUIRED_KEYS in env! Got: '{req_keys_s}'")
        req_keys = json.loads(req_keys_s)
        if type(req_keys) is not list:
            raise Exception(
                f"Could not parse REQUIRED_KEYS into list! Got: '{req_keys}'"
            )
        for k in req_keys:
            if type(k) is not str:
                raise Exception(
                    f"Could not parse REQUIRED_KEYS into list of strings! Got: '{req_keys}'"
                )
        self.req_keys = req_keys

        error_webhook_url = os.environ.get("ERROR_WEBHOOK_URL")
        if error_webhook_url is None:
            raise Exception(
                f"Could not find ERROR_WEBHOOK_URL in env! Got: '{error_webhook_url}'"
            )
        error_webhook_url = error_webhook_url.strip()
        if error_webhook_url == "":
            raise Exception(
                f"Could not parse ERROR_WEBHOOK_URL into non-empty string! Got: '{error_webhook_url}'"
            )
        self.error_webhook_url = error_webhook_url

        webhook_url = os.environ.get("TEAMS_WEBHOOK_URL")
        if webhook_url is None:
            raise Exception(
                f"Could not find TEAMS_WEBHOOK_URL in env! Got: '{webhook_url}'"
            )
        webhook_url = webhook_url.strip()
        if webhook_url == "":
            raise Exception(
                f"Could not parse TEAMS_WEBHOOK_URL into non-empty string! Got: '{webhook_url}'"
            )
        self.webhook_url = webhook_url
