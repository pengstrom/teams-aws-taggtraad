import requests as r
from dotenv import load_dotenv
import adaptive_card as s
import os

from .teams import WebhookBody

def create_message(msg: str) -> WebhookBody:
    block = s.TextBlock(text = msg)
    card = s.AdaptiveCard(body = [block]) # type: ignore
    item = s.AdaptiveCardItem(content = card)
    return WebhookBody(attachments=[item])

def main():
    load_dotenv()
    url = os.getenv("TEAMS_WEBHOOK_URL")
    if not url:
        raise Exception("No TEAMS_WEBHOOK_URL env var found!")
    
    body = create_message("foo")
    res = r.post(url, json=body.model_dump(by_alias=True, serialize_as_any=True))
    res.raise_for_status()

if __name__ == "__main__":
    main()