import os

from fastapi import FastAPI, Request, HTTPException
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler


TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

app = FastAPI()

telegram_app = Application.builder().token(TOKEN).build()


async def start(update: Update, context):

    keyboard = [
        [
            InlineKeyboardButton(
                "Open My Course",
                web_app=WebAppInfo(
                    url="https://telegram-mini-app-two-xi.vercel.app"
                )
            )
        ]
    ]

    await update.message.reply_text(
        "🎓 Welcome to Your Learning Journey!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


telegram_app.add_handler(CommandHandler("start", start))


@app.get("/")
async def home():
    return {"status": "Telegram bot server is running"}


@app.post("/webhook")
async def webhook(request: Request):

    secret = request.headers.get(
        "X-Telegram-Bot-Api-Secret-Token"
    )

    if secret != WEBHOOK_SECRET:
        raise HTTPException(status_code=403)

    data = await request.json()

    update = Update.de_json(data, telegram_app.bot)

    await telegram_app.process_update(update)

    return {"ok": True}


@app.on_event("startup")
async def startup():

    await telegram_app.initialize()
    await telegram_app.start()

    render_url = os.getenv("RENDER_EXTERNAL_URL")

    await telegram_app.bot.set_webhook(
        url=f"{render_url}/webhook",
        secret_token=WEBHOOK_SECRET
    )

    print("Telegram webhook configured")


@app.on_event("shutdown")
async def shutdown():

    await telegram_app.bot.delete_webhook()

    await telegram_app.stop()
    await telegram_app.shutdown()