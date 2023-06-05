import os
from typing import List
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from aiogram import Bot, types

class Author(BaseModel):
    name: str
    email: str

class Commit(BaseModel):
    id: str
    message: str
    timestamp: str
    url: str
    author: Author

class WebhookCommit(BaseModel):
    commits: List[Commit]
    ref: str

class MR(BaseModel):
    id: int
    target_branch: str
    source_branch: str
    url: str

class WebhookMR(BaseModel):
    object_attributes: MR

app = FastAPI()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = Bot(token=TELEGRAM_TOKEN)

@app.post("/webhook/commit")
async def gitlab_commits_webhook(commit: Commit):
    ref = commit.ref
    ref_escaped = ref.replace("_", "\\\\_")
    for commit_info in commit.commits:
        url = commit_info.url
        message_escaped = commit_info.message.replace("_", "\\\\_")
        message = f"[Nuevo commit en {ref_escaped}: '{message_escaped}' por {commit_info.author.name}]({url})"
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode='Markdown')
    return {"message": "OK"}

@app.post("/webhook/mr")
async def gitlab_webhook_mr(webhook: WebhookMR):
    if webhook.object_attributes.target_branch == 'dev':
        message = f"Nuevo Merge Request: '{webhook.object_attributes.source_branch}' a 'dev'. URL: {webhook.object_attributes.url}"
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "OK"})

@app.post("/webhook/echo")
async def gitlab_webhook_echo():
    return {"message": "OK"}
