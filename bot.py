import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# Read secrets from environment (IMPORTANT)
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
VIP_LINK = os.getenv("VIP_LINK")


# START MESSAGE
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "To join our VIP group:\n"
        "1. Open & fund your trading account\n"
        "2. Send a screenshot here\n\n"
        "We manually review all submissions."
    )


# RECEIVE SCREENSHOT
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user.id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}")
        ]
    ])

    photo = update.message.photo[-1].file_id

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo,
        caption=f"New user:\n{user.first_name}\n@{user.username}\nID: {user.id}",
        reply_markup=keyboard
    )

    await update.message.reply_text("📩 Received. Waiting for approval.")


# BUTTON HANDLER
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, user_id = query.data.split("_")
    user_id = int(user_id)

    if query.from_user.id != ADMIN_ID:
        return

    if action == "approve":
        await context.bot.send_message(
            chat_id=user_id,
            text=f"✅ Approved!\n\nHere is your VIP access:\n{VIP_LINK}"
        )
        await query.edit_message_caption(query.message.caption + "\n\nAPPROVED")

    elif action == "reject":
        await context.bot.send_message(
            chat_id=user_id,
            text="❌ Not approved. Please try again with valid proof."
        )
        await query.edit_message_caption(query.message.caption + "\n\nREJECTED")


# MAIN APP
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
