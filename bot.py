import telebot
import os
import re
from deep_translator import GoogleTranslator

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    print("❌ Missing BOT_TOKEN")
    exit(1)

bot = telebot.TeleBot(TOKEN)

# ===== START =====
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "🤖 Bot tính toán & dịch Nhật → Việt\n\n"
        "📌 Ví dụ:\n"
        "1+2+3\n"
        "10.5*2\n"
        "100/4\n\n"
        "🇯🇵 Gửi tiếng Nhật → bot tự dịch"
    )

# ===== KIỂM TRA BIỂU THỨC TOÁN =====
math_pattern = re.compile(r'^[0-9\.\+\-\*\/\(\)\s]+$')

def safe_eval(expr):
    return eval(expr, {"__builtins__": None}, {})

# ===== XỬ LÝ TIN NHẮN =====
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    text = message.text.strip()

    # 1️⃣ TOÁN
    if math_pattern.match(text):
        try:
            result = safe_eval(text)
            bot.reply_to(message, f"= {result}")
            return
        except:
            pass

    # 2️⃣ DỊCH NHẬT → VIỆT
    try:
        translated = GoogleTranslator(source='ja', target='vi').translate(text)
        if translated and translated.lower() != text.lower():
            bot.reply_to(message, f"🇯🇵➡️🇻🇳 {translated}")
    except:
        pass


print("✅ Bot is running...")
bot.infinity_polling()
