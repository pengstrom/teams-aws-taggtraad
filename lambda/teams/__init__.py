import requests as r
from teams.adaptive_card import *
from pydantic import BaseModel
from logger import logger

class WebhookBody(BaseModel):
    type: str = "message"
    attachments: list[AdaptiveCardItem]


class Webhook:
    url: str

    def __init__(self, url):
        self.url = url

    def send(self, card: AdaptiveCard):
        webhook_body = WebhookBody(attachments=[AdaptiveCardItem(content=card)])
        body = webhook_body.model_dump(by_alias=True, serialize_as_any=True, exclude_none=True)
        logger.debug("Dumped body:")
        logger.debug(body)
        res = r.post(self.url, json=body)
        res.raise_for_status()
        logger.debug("Response")
        logger.debug(res)
