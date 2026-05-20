from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8638894950:AAGICO_hfb2YogDeJf06x7PPPIDPqG28Hx0"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "Open My Course",
                web_app=WebAppInfo(url="https://yourwebsite.vercel.app")
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🎓 Welcome to Your Learning Journey!",
        reply_markup=reply_markup
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

print("Bot Running...")
app.run_polling()