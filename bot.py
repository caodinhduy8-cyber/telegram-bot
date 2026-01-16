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
from deep_translator import GoogleTranslator

# kiểm tra có phải tiếng Nhật không
def is_japanese(text):
    return bool(re.search(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]', text))

@bot.message_handler(func=lambda m: m.text and is_japanese(m.text))
def translate_jp_to_vi(message):
    try:
        translated = GoogleTranslator(source='ja', target='vi').translate(message.text)
        bot.reply_to(message, f"🇯🇵→🇻🇳 {translated}")
    except:
        bot.reply_to(message, "❌ Không dịch được")
bot.infinity_polling()
