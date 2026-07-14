import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = os.environ.get("ADMIN_ID")

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing.")

if not ADMIN_ID:
    raise ValueError("ADMIN_ID environment variable is missing.")

ADMIN_ID = int(ADMIN_ID)

users = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 به پشتیبانی فارسی دل خوش آمدید!\n\n"
        "لطفاً پیام خود را ارسال کنید."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message or not update.message.text:
        return

    user = update.effective_user
    chat_id = update.effective_chat.id
    text = update.message.text

    # Admin messages
    if chat_id == ADMIN_ID:
        await update.message.reply_text(
            "برای پاسخ:\n\n"
            "/reply USER_ID پیام"
        )
        return

    users[user.id] = True

    username = f"@{user.username}" if user.username else "None"

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"""
📩 New Support Message

👤 Name:
{user.first_name}

🔗 Username:
{username}

🆔 User ID:
{user.id}

💬 Message:

{text}

------------------------

Reply with:

/reply {user.id} your message
"""
    )

    await update.message.reply_text(
        "✅ پیام شما ارسال شد.\n\n"
        "پشتیبانی به زودی پاسخ خواهد داد."
    )


async def reply_customer(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_chat.id != ADMIN_ID:
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage:\n\n"
            "/reply USER_ID message"
        )
        return

    try:

        user_id = int(context.args[0])

        message = " ".join(context.args[1:])

        await context.bot.send_message(
            chat_id=user_id,
            text=f"💬 پشتیبانی فارسی دل\n\n{message}"
        )

        await update.message.reply_text("✅ Reply sent.")

    except Exception as e:

        await update.message.reply_text(f"Error: {e}")


def main():

    print("===================================")
    print("🚀 Starting Farsidle Support Bot...")
    print(f"👤 Admin ID: {ADMIN_ID}")
    print("===================================")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reply", reply_customer))
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message,
        )
    )

    print("✅ Support bot is running...")

    app.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()