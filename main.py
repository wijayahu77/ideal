from fastapi import FastAPI, Request
import openai
import os
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import asyncio

TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_KEY
bot = Bot(token=TOKEN)
app = FastAPI()

@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, bot)
    if update.message:
        user_msg = update.message.text
        chat_id = update.message.chat.id

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_msg}]
        )

        reply = response['choices'][0]['message']['content']
        await bot.send_message(chat_id=chat_id, text=reply)
    return {"ok": True}
