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


load_dotenv()

TOKEN = os.environ.get("BOT_TOKEN")

# Your Telegram ID
ADMIN_ID = 1200652625


# FastAPI app for Render
web_app = FastAPI()


@web_app.get("/")
def home():
    return {
        "status": "Farsidle Support Bot is running"
    }


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "به پشتیبانی فارسی دل خوش آمدید 🌱\n\n"
        "لطفاً پیام خود را ارسال کنید."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user

    # Ignore admin messages
    if update.message.chat.id == ADMIN_ID:
        return


    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"""
📩 New Support Message

Name:
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

        message = " ".join(context.args[1:])


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



async def error_handler(update, context):

    print(
        f"Error: {context.error}"
    )



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

    await telegram_app.initialize()

    await telegram_app.start()

    await telegram_app.updater.start_polling()



def start_bot():

    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)

    loop.run_until_complete(
        run_bot()
    )



Thread(
    target=start_bot,
    daemon=True
).start()