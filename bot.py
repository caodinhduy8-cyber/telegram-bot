import telebot
import os
import re

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    print("❌ Missing BOT_TOKEN")
    exit(1)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "🧮 Bot tính toán\n"
        "Ví dụ:\n"
        "1+2+3\n"
        "10.5-2.3\n"
        "5*2*3\n"
        "10/2/2"
    )

@bot.message_handler(func=lambda m: True)
def calc(message):
    text = message.text.replace(" ", "")

    # chỉ cho phép số + - * / .
    if not re.fullmatch(r"[0-9+\-*/.]+", text):
        return

    try:
        result = eval(text)
        bot.reply_to(message, f"= {result}")
    except:
        bot.reply_to(message, "❌ Biểu thức không hợp lệ")

print("✅ Bot is running...")
bot.infinity_polling()
