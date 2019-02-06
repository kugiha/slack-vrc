from flask import Flask, request, make_response, Response
import os
import json

from slackclient import SlackClient

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_VERIFICATION_TOKEN = os.environ.get("SLACK_VERIFICATION_TOKEN")
slack_client = SlackClient(SLACK_BOT_TOKEN)
app = Flask(__name__)

@app.route("/slash/", methods=["POST"])
def commands():
    slack_client.api_call(
        "chat.postMessage",
        channel="#general",
        text="あなたはどっち派？"
    )
    return make_response("", 200)