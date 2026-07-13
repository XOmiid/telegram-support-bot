import os
import asyncio
from threading import Thread

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


# Load environment variables
load_dotenv()

TOKEN = os.environ.get("BOT_TOKEN")

# Your Telegram ID
ADMIN_ID = 1200652625


print("BOT TOKEN LOADED:", TOKEN[:10] if TOKEN else "NO TOKEN")


# FastAPI app for Render
web_app = FastAPI()


@web_app.get("/")
def home():
    return {
        "status": "Farsidle Support Bot is running"
    }


# =========================
# Telegram Commands
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "به پشتیبانی فارسی دل خوش آمدید 🌱\n\n"
        "لطفاً پیام خود را ارسال کنید."
    )


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.message.from_user

    # Ignore admin messages
    if update.message.chat.id == ADMIN_ID:
        return


    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"""
📩 پیام جدید پشتیبانی

👤 Name:
{user.first_name}

🔗 Username:
@{user.username}

🆔 User ID:
{user.id}


💬 Message:

{update.message.text}


برای پاسخ:

/reply {user.id} پیام شما
"""
    )


    await update.message.reply_text(
        "پیام شما ارسال شد ✅\n\n"
        "پشتیبانی به زودی پاسخ خواهد داد."
    )



async def reply_customer(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

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
            "پاسخ ارسال شد ✅"
        )


    except Exception:

        await update.message.reply_text(
            "فرمت صحیح:\n\n"
            "/reply USER_ID message"
        )



async def error_handler(
    update,
    context
):

    print(
        "Telegram Error:",
        context.error
    )



# =========================
# Telegram Bot Setup
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


telegram_app.add_error_handler(
    error_handler
)



async def run_bot():

    print("Initializing Telegram bot...")

    await telegram_app.initialize()

    await telegram_app.start()

    await telegram_app.updater.start_polling()

    print("Telegram polling started")



def start_bot():

    print("Starting Telegram bot thread...")

    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)

    try:

        loop.run_until_complete(
            run_bot()
        )

    except Exception as e:

        print(
            "BOT START ERROR:",
            e
        )



# Start bot in background thread

bot_thread = Thread(
    target=start_bot,
    daemon=True
)


bot_thread.start()


print("Telegram bot thread started")