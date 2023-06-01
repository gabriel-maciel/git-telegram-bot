import os
import flask
from flask import request
from telegram import Bot

# Obtiene los tokens desde las variables de entorno
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=TELEGRAM_TOKEN)

app = flask.Flask(__name__)

@app.route('/webhook', methods=['POST'])
def gitlab_webhook():
    print("hello?")
    app.logger.info("Webhook received")
    bot.send_message(chat_id=os.getenv('TELEGRAM_CHAT_ID'), text='Test webhook')
    if request.method == 'POST':
        json = request.get_json()
        ref = json['ref']
        if 'master' in ref or 'dev' in ref:
            commits = json['commits']
            for commit in commits:
                message = f"Nuevo commit en {ref}: {commit['message']} por {commit['author']['name']}"
                app.logger.info(message)
                bot.send_message(chat_id=os.getenv('TELEGRAM_CHAT_ID'), text=message)
        return 'OK', 200
    else:
        return 'OK', 200

@app.route("/webhook-echo", methods=["POST"])
def gitlab_webhook_echo():    
    return "OK"

if __name__ == "__main__":
    port = int(os.getenv('PORT', 7876))
    app.run(host='0.0.0.0', port=port)

