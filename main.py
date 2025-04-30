from fastapi import FastAPI, Request
import openai
import os
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import asyncio

TOKEN = os.getenv("7779294054:AAHKbTwTe1qT2AeOaSy-dhQviqmRgx1squE")
OPENAI_KEY = os.getenv("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")

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
