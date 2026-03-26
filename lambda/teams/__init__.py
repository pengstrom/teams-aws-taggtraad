import requests as r
from adaptive_card import *
from pydantic import BaseModel
import json


class WebhookBody(BaseModel):
    type: str = "message"
    attachments: list[AdaptiveCardItem]


class Webhook:
    url: str

    def __init__(self, url):
        self.url = url

    def send(self, card: AdaptiveCard):
        webhook_body = WebhookBody(attachments=[AdaptiveCardItem(content=card)])
        body = webhook_body.model_dump(by_alias=True, serialize_as_any=True)
        print("Body:")
        print(webhook_body.model_dump_json(indent=2, by_alias=True, serialize_as_any=True))
        res = r.post(self.url, json=body)
        res.raise_for_status()
