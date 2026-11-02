import telebot
from telebot import types
import threading
from flask import Flask
import os

# --- SOZLAMALAR ---
BOT_TOKEN = "9005189458:AAGqu4mvsRvHNXVaG7gXzvUfP8eYerdQmJU" 
INSTAGRAM_URL = "https://instagram.com/bek_oka_9999"
CHANNEL_ID = "@kinolarolami9999"
CHANNEL_LINK = "https://t.me/kinolarolami9999"

bot = telebot.TeleBot(BOT_TOKEN)

app = Flask('')

@app.route('/')
def home():
    return "Bot ishlayapti!"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_insta = types.InlineKeyboardButton("📸 Instagramga obuna bo'lish", url=INSTAGRAM_URL)
    btn_channel = types.InlineKeyboardButton("📢 Telegram kanalga obuna bo'lish", url=CHANNEL_LINK)
    btn_check = types.InlineKeyboardButton("✅ Tasdiqlash", callback_data="check_sub")
    markup.add(btn_insta, btn_channel, btn_check)
    
    text = ("🎬 *Kinoni to'liq ko'rish uchun:*\n\n"
            "1️⃣ Instagram sahifamizga obuna bo'ling\n"
            "2️⃣ Telegram kanalimizga obuna bo'ling\n"
            "3️⃣ «Tasdiqlash» tugmasini bosing\n\n"
            "Shundan so'ng kino havolasini olasiz! 🍿")
    
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_sub(call):
    user_id = call.from_user.id
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ["member", "administrator", "creator"]:
            bot.answer_callback_query(call.id, "✅ Tasdiqlandi!")
            bot.send_message(user_id, 
                f"🎉 Rahmat! Siz tasdiqlandingiz.\n\n"
                f"Mana kinoni ko'rishingiz mumkin: {CHANNEL_LINK}\n\n"
                f"Yangi kinolar uchun kanalni kuzatib boring!")
        else:
            bot.answer_callback_query(call.id, "❌ Avval Telegram kanalga obuna bo'ling!", show_alert=True)
    except Exception as e:
        bot.answer_callback_query(call.id, "⚠️ Xatolik! Iltimos, kanalga obuna bo'lganingizni tekshiring.", show_alert=True)

if __name__ == "__main__":
    threading.Thread(target=run).start()
    print("Bot ishga tushdi...")
    bot.infinity_polling()
