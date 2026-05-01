import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from flask import Flask

app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
VIP_LINK = "https://t.me/yourVIPgroup"

bot = telebot.TeleBot(TOKEN)


# ================= TELEGRAM BOT =================
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Welcome 🚀\n\n"
        "Open broker + deposit $300 + send screenshot via /submit"
    )


@bot.message_handler(commands=['submit'])
def submit(message):
    bot.send_message(message.chat.id, "Send your screenshot 📸")


@bot.message_handler(content_types=['photo'])
def photo(message):
    file_id = message.photo[-1].file_id

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("✅ Approve", callback_data=f"approve_{message.chat.id}"),
        InlineKeyboardButton("❌ Decline", callback_data=f"decline_{message.chat.id}")
    )

    bot.send_photo(
        ADMIN_ID,
        file_id,
        caption=f"User: {message.chat.id}",
        reply_markup=markup
    )

    bot.send_message(message.chat.id, "Received ✅")


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    action, user_id = call.data.split("_")
    user_id = int(user_id)

    if action == "approve":
        bot.send_message(user_id, f"Approved 🎉\n{VIP_LINK}")
    else:
        bot.send_message(user_id, "Not approved ❌")


# ================= KEEP RENDER ALIVE =================
@app.route("/")
def home():
    return "Bot is running"


if __name__ == "__main__":
    from threading import Thread

    def run_bot():
        bot.infinity_polling()

    Thread(target=run_bot).start()

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
