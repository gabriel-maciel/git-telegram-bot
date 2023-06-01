import os
from fastapi import FastAPI
from telegram import Bot
from starlette.requests import Request

app = FastAPI()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=TELEGRAM_TOKEN)

@app.post('/webhook')
async def gitlab_webhook(request: Request):
    print("hello?")
    await bot.send_message(chat_id=os.getenv('TELEGRAM_CHAT_ID'), text='Webhook received')

    json = await request.json()
    ref = json['ref']
    if 'master' in ref or 'dev' in ref:
        commits = json['commits']
        for commit in commits:
            message = f"Nuevo commit en {ref}: {commit['message']} por {commit['author']['name']}"
            print(message)
            await bot.send_message(chat_id=os.getenv('TELEGRAM_CHAT_ID'), text=message)

    return {"message": "OK"}

@app.post("/webhook-echo")
async def gitlab_webhook_echo():    
    return {"message": "OK"}
