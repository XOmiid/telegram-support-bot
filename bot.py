import os
import asyncio

from dotenv import load_dotenv
from fastapi import FastAPI

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)


load_dotenv()

TOKEN = os.environ.get("BOT_TOKEN")

ADMIN_ID = 1200652625


print(
    "BOT TOKEN LOADED:",
    TOKEN[:10] if TOKEN else "NO TOKEN"
)


# =========================
# FastAPI
# =========================

web_app = FastAPI()


@web_app.get("/")
def home():
    return {
        "status": "Farsidle Support Bot is running"
    }



# =========================
# Telegram handlers
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "به پشتیبانی فارسی دل خوش آمدید 🌱\n\n"
        "لطفاً پیام خود را ارسال کنید."
    )



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user


    if update.message.chat.id == ADMIN_ID:
        return


    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"""
📩 پیام جدید پشتیبانی

👤 Name:
{user.first_name}

Username:
@{user.username}

User ID:
{user.id}


Message:

{update.message.text}


Reply:

/reply {user.id} your message
"""
    )


    await update.message.reply_text(
        "پیام شما ارسال شد ✅"
    )



async def reply_customer(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.chat.id != ADMIN_ID:
        return


    try:

        user_id = int(context.args[0])

        message = " ".join(
            context.args[1:]
        )


        await context.bot.send_message(
            chat_id=user_id,
            text=f"""
پشتیبانی فارسی دل:

{message}
"""
        )


        await update.message.reply_text(
            "ارسال شد ✅"
        )


    except:

        await update.message.reply_text(
            "Format:\n/reply USER_ID message"
        )



# =========================
# Telegram application
# =========================

telegram_app = (
    Application
    .builder()
    .token(TOKEN)
    .build()
)


telegram_app.add_handler(
    CommandHandler(
        "start",
        start
    )
)


telegram_app.add_handler(
    CommandHandler(
        "reply",
        reply_customer
    )
)


telegram_app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_message
    )
)



# =========================
# Start Telegram with FastAPI
# =========================

@web_app.on_event("startup")
async def startup():

    print("Starting Telegram bot...")

    await telegram_app.initialize()

    await telegram_app.start()

    await telegram_app.updater.start_polling()

    print("Telegram polling started")



@web_app.on_event("shutdown")
async def shutdown():

    print("Stopping Telegram bot...")

    await telegram_app.updater.stop()

    await telegram_app.stop()

    await telegram_app.shutdown()