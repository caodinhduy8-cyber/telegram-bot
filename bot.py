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

# lấy username bot
BOT_USERNAME = bot.get_me().username.lower()

# ===== START =====
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "🤖 Bot tính toán & dịch Nhật → Việt\n\n"
        "📌 Dùng trong group cần TAG bot:\n"
        f"@{BOT_USERNAME} 1,2+1,5\n"
        f"@{BOT_USERNAME} 99,9+50+36,8\n"
        f"@{BOT_USERNAME} 明日ピックルボールをします"
    )

# ===== HÀM TÍNH TOÁN =====
def calc_expression(expr):
    try:
        # đổi dấu , thành .
        expr = expr.replace(",", ".")

        # chỉ cho phép số & toán tử
        if not re.fullmatch(r"[0-9+\-*/().\s]+", expr):
            return None

        result = eval(expr)

        # làm gọn số
        if isinstance(result, float):
            result = round(result, 10)
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

    text = message.text

    # ===== CHỈ TRẢ LỜI KHI BỊ TAG =====
    mentioned = False
    if message.entities:
        for e in message.entities:
            if e.type == "mention":
                mention_text = text[e.offset:e.offset + e.length].lower()
                if mention_text == f"@{BOT_USERNAME}":
                    mentioned = True
                    break

    if not mentioned:
        return  # ❌ không tag → im lặng

    # bỏ tag ra khỏi nội dung
    text = re.sub(f"@{BOT_USERNAME}", "", text, flags=re.IGNORECASE).strip()

    # ===== DỊCH TIẾNG NHẬT =====
    if re.search(r"[\u3040-\u30ff\u4e00-\u9fff]", text):
        try:
            vi = translator.translate(text)
            bot.reply_to(message, f"🇯🇵 ➡ 🇻🇳 {vi}")
            return
        except:
            pass

    # ===== TÍNH TOÁN =====
    result = calc_expression(text)
    if result is not None:
        bot.reply_to(message, f"= {result}")

# ===== RUN =====
print("✅ Bot is running...")
bot.infinity_polling()
