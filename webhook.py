from flask import Flask, request
import json
import os
from dotenv import load_dotenv
load_dotenv()

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    ImageMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)

access_token = os.getenv("ACCESS_TOKEN")
channel_secret = os.getenv("CHANNEL_SECRET")

configuration = Configuration(access_token=access_token)
handler = WebhookHandler(channel_secret=channel_secret)

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return "Invalid signature", 400

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        reply_message_request = ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=event.message.text)]
        )
        line_bot_api.reply_message(reply_message_request)

'''
@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        reply_message_request = ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text="画像を受信しました")]
        )
        line_bot_api.reply_message(reply_message_request)
'''
if __name__ == "__main__":
    app.run()