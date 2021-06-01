import json

import requests
from django.conf import settings

def _send_slack_message(webhook_url, channel_name, bot_username, icon_emoji, text, attachments):
    """
    Generic function that sends a Slack message via incoming webhook.
    Set up your own incoming webhook at: https://api.slack.com/incoming-webhooks#sending_messages
    """
    return requests.post(
        url=webhook_url,
        headers={"content-type": "application/json"},
        data=json.dumps(
            {
                "channel": channel_name,
                "username": bot_username,
                "icon_emoji": icon_emoji,
                "text": text,
                "attachments": attachments,
            }
        ),
    )


def send_slack_log_message(text, attachments=[]):
    """
    Sends log messages to slack.
    Do not forget to create a webhook in your slack settings and update the INCOMING_WEBHOOK_URL accordingly in settings.py.

    Usage example:
    send_slack_log_message("wesh")
    """
    return _send_slack_message(
        webhook_url=settings.SLACK_LOGS_CHANNEL_INCOMING_WEBHOOK_URL,
        channel_name=settings.SLACK_LOGS_CHANNEL_NAME,
        bot_username=settings.SLACK_LOGS_BOT_USERNAME,
        icon_emoji=settings.SLACK_LOGS_BOT_ICON_EMOJI,
        text=text,
        attachments=attachments,
    )
