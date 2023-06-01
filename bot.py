import os
import flask
from flask import request
from telegram import Bot

# Obtiene los tokens desde las variables de entorno
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=TELEGRAM_TOKEN)

app = flask.Flask(__name__)

@app.route("/webhook", methods=["POST"])
def gitlab_webhook():
    data = request.get_json()

    if data['object_kind'] == 'merge_request':
        attributes = data['object_attributes']
        if attributes['target_branch'] == 'dev' and attributes['state'] == 'merged':
            bot.send_message(chat_id=CHAT_ID, text="Se ha realizado un merge a dev")
    
    return "OK"

if __name__ == "__main__":
    app.run(port=5000)
