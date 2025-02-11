import os

import requests


def send_webhook(message: str) -> None:
    webhook_url = os.environ.get("WEBHOOK_URL")
    if webhook_url is None:
        msg = "WEBHOOK_URL is not set"
        raise ValueError(msg)

    requests.post(webhook_url, data={"content": message}, timeout=5)
