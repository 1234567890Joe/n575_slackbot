# -*- coding: utf-8 -*-

import os
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from n575_detector import n575_detector

# Initialize a Flask app to host the events adapter
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(
    os.environ["SLACK_SIGNING_SECRET"], "/slack/events", app)

# Initialize a Web API client
slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

# Make BOT Users List
BOTS = []
for i in slack_web_client.users_list().get("members"):
    if i.get("is_bot") is True:
        BOTS.append(i.get("id"))


@slack_events_adapter.on("message")
def message(payload):
    event = payload.get("event", {})

    channel_id = event.get("channel")
    user_id = event.get("user")
    print(BOTS, user_id)
    if user_id not in BOTS:
        text = event.get("text")
        haikus = n575_detector(text)
        if len(haikus) != 0:
            for i in haikus:
                slack_web_client.chat_postMessage(
                    channel=channel_id, text=i
                )


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(port=3000)
