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

# For simplicity we'll store our app data in-memory with the following data structure.
# onboarding_tutorials_sent = {"channel": {"user_id": OnboardingTutorial}}
onboarding_tutorials_sent = {}
BOTS = []
for i in slack_web_client.users_list().get("members"):
    if i.get("is_bot") is True:
        BOTS.append(i.get("id"))

# ============== Message Events ============= #
# When a user sends a DM, the event type will be 'message'.
# Here we'll link the message callback to the 'message' event.
@slack_events_adapter.on("message")
def message(payload):
    """Display the onboarding welcome message after receiving a message
    that contains "start".
    """
    event = payload.get("event", {})

    channel_id = event.get("channel")
    user_id = event.get("user")
    if user_id in BOTS:
        return 0
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
