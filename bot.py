import telebot
import os
import re
import requests

# ===== TOKEN =====
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    print("❌ Missing BOT_TOKEN")
    exit(1)

bot = telebot.TeleBot(TOKEN)

# lấy username bot
BOT_USERNAME = bot.get_me().username.lower()

# ===== START =====
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "🤖 Bot tính toán & giá USDT/VND\n\n"
        "📌 Cách dùng:\n"
        "• Chat riêng: gõ trực tiếp\n"
        f"• Group: tag @{BOT_USERNAME} hoặc reply bot\n\n"
        "Ví dụ:\n"
        "👉 1,2+3,5\n"
        "👉 usdt"
    )

# ===== HÀM TÍNH TOÁN =====
def calc_expression(expr):
    try:
        expr = expr.replace(",", ".")
        if not re.fullmatch(r"[0-9+\-*/().\s]+", expr):
            return None

        result = eval(expr)

        if isinstance(result, float):
            result = round(result, 10)
            if result.is_integer():
                result = int(result)

        return result
    except:
        return None

# ===== HÀM GIÁ USDT =====
def get_usdt_vnd():
    try:
        url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
        payload = {
            "asset": "USDT",
            "fiat": "VND",
            "merchantCheck": False,
            "page": 1,
            "rows": 5,
            "tradeType": "BUY"
        }
        headers = {"Content-Type": "application/json"}

        res = requests.post(url, json=payload, headers=headers, timeout=5)
        data = res.json()

        prices = [float(i["adv"]["price"]) for i in data["data"]]
        avg_price = sum(prices) / len(prices)

        return int(avg_price)
    except:
        return None

# ===== XỬ LÝ TIN NHẮN =====
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    if not message.text:
        return

    text = message.text.strip()

    # ===== ĐIỀU KIỆN TRẢ LỜI =====
    is_private = message.chat.type == "private"

    is_mentioned = False
    if message.entities:
        for e in message.entities:
            if e.type == "mention":
                mention_text = text[e.offset:e.offset + e.length].lower()
                if mention_text == f"@{BOT_USERNAME}":
                    is_mentioned = True
                    break

    is_reply_to_bot = (
        message.reply_to_message
        and message.reply_to_message.from_user
        and message.reply_to_message.from_user.username
        and message.reply_to_message.from_user.username.lower() == BOT_USERNAME
    )

    if not (is_private or is_mentioned or is_reply_to_bot):
        return

    # bỏ tag bot
    text = re.sub(f"@{BOT_USERNAME}", "", text, flags=re.IGNORECASE).strip()
    if not text:
        return

    # ===== GIÁ USDT =====
    if re.search(r"\busdt\b", text.lower()):
        price = get_usdt_vnd()
        if price:
            bot.reply_to(
                message,
                f"💵 USDT/VND\n≈ {price:,} ₫\n(Nguồn: Binance P2P)"
            )
        else:
            bot.reply_to(message, "❌ Không lấy được giá USDT")
        return

    # ===== TÍNH TOÁN =====
    result = calc_expression(text)
    if result is not None:
        bot.reply_to(message, f"= {result}")

# ===== RUN =====
print("✅ Bot is running...")
bot.infinity_polling()
