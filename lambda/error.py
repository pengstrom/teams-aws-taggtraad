from config import AppConfig
from adaptive_card import *
from teams import *


def report_error(cfg: AppConfig, err):
    text = str(err)
    client = Webhook(cfg.error_webhook_url)
    block = TextBlock(text=text)
    card = AdaptiveCard(body=[block])  # pyright: ignore[reportCallIssue]
    client.send(card)
