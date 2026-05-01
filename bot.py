import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
VIP_LINK = "https://t.me/yourVIPgroup"

bot = telebot.TeleBot(TOKEN)


# ================= START =================
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Welcome to Madlab Trading 🚀\n\n"
        "To access VIP signals:\n\n"
        "1. Open a broker account\n"
        "2. Deposit minimum $300\n"
        "3. Send screenshot using /submit\n\n"
        "BlackBull (NZ only):\n"
        "https://blackbull.com/en/live-account/?cmp=5p0z2d3q&refid=6509\n\n"
        "HeroFX:\n"
        "https://herofx.co/?partner_code=4649955"
    )


# ================= SUBMIT =================
@bot.message_handler(commands=['submit'])
def submit(message):
    bot.send_message(message.chat.id, "Please send your screenshot 📸")


# ================= HANDLE PHOTO =================
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id

    markup = InlineKeyboardMarkup()
    approve = InlineKeyboardButton("✅ Approve", callback_data=f"approve_{message.chat.id}")
    decline = InlineKeyboardButton("❌ Decline", callback_data=f"decline_{message.chat.id}")
    markup.add(approve, decline)

    bot.send_photo(
        ADMIN_ID,
        file_id,
        caption=f"New verification request\nUser: {message.chat.id}",
        reply_markup=markup
    )

    bot.send_message(message.chat.id, "Screenshot received ✅ under review")


# ================= ADMIN ACTION =================
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    action, user_id = call.data.split("_")
    user_id = int(user_id)

    if action == "approve":
        bot.send_message(user_id, f"Approved 🎉\n\nVIP Access:\n{VIP_LINK}")
        bot.answer_callback_query(call.id, "Approved")

    elif action == "decline":
        bot.send_message(user_id, "Not approved ❌ Please resend clearer proof.")
        bot.answer_callback_query(call.id, "Declined")


# ================= RUN BOT =================
bot.infinity_polling()
