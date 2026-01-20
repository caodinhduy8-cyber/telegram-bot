import telebot
import os
import re
from deep_translator import GoogleTranslator

# ===== TOKEN =====
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    print("❌ Missing BOT_TOKEN")
    exit(1)

bot = telebot.TeleBot(TOKEN)
translator = GoogleTranslator(source="ja", target="vi")

# ===== START =====
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "🤖 Bot tính toán & dịch Nhật → Việt\n\n"
        "📌 Ví dụ:\n"
        "@tenbot 1+2*3\n"
        "@tenbot 1.2+1.3+199.7\n"
        "@tenbot 明日ピックルボールをします"
    )

# ===== HÀM TÍNH TOÁN =====
def calc_expression(expr):
    try:
        if not re.fullmatch(r"[0-9+\-*/().\s]+", expr):
            return None

        result = eval(expr)

        # làm gọn số
        if isinstance(result, float):
            result = round(result, 6)
            if result.is_integer():
                result = int(result)

        return result
    except:
        return None

# ===== XỬ LÝ TIN NHẮN =====
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    if not message.text:
        return

    text = message.text.strip()

    # 🔒 CHỈ TRẢ LỜI KHI BỊ TAG TRONG GROUP
    if message.chat.type in ["group", "supergroup"]:
        bot_username = bot.get_me().username
        if f"@{bot_username}" not in text:
            return
        text = text.replace(f"@{bot_username}", "").strip()

    # 1️⃣ DỊCH TIẾNG NHẬT
    if re.search(r"[\u3040-\u30ff\u4e00-\u9fff]", text):
        try:
            vi = translator.translate(text)
            bot.reply_to(message, f"🇯🇵 ➡ 🇻🇳 {vi}")
            return
        except:
            pass

    # 2️⃣ TÍNH TOÁN
    result = calc_expression(text)
    if result is not None:
        bot.reply_to(message, f"= {result}")

# ===== RUN =====
print("✅ Bot is running...")
bot.infinity_polling()
