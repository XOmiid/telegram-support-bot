import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)


TOKEN = os.environ.get("BOT_TOKEN")

# YOUR personal Telegram ID
ADMIN_ID = 1200652625


# Stores users temporarily
users = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        " به پشتیبانی فارسی دل خوش آمدی!\n\nنظر یا سوالی دارین لطفا پیامتون رو بنوسید:"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user
    chat_id = update.message.chat.id
    text = update.message.text


    # If message comes from customer
    if chat_id != ADMIN_ID:

        users[user.id] = user.id


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

{text}


Reply using:
 /reply USER_ID message
"""
        )


        await update.message.reply_text(
            "پیام شما ارسال شد!"
        )


    # If message comes from you
    else:

        await update.message.reply_text(
            "Use /reply USER_ID message to answer a customer."
        )



async def reply_customer(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.chat.id != ADMIN_ID:
        return


    try:

        customer_id = int(context.args[0])

        message = " ".join(context.args[1:])


        await context.bot.send_message(
            chat_id=customer_id,
            text=f"Support:\n\n{message}"
        )


        await update.message.reply_text(
            "Reply sent ✅"
        )


    except:

        await update.message.reply_text(
            "Format:\n/reply USER_ID your message"
        )



app = Application.builder().token(TOKEN).build()


app.add_handler(CommandHandler("start", start))

app.add_handler(
    CommandHandler("reply", reply_customer)
)

app.add_handler(
    MessageHandler(
        filters.TEXT,
        handle_message
    )
)


print("Support bot running...")

app.run_polling()
