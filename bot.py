import telebot
import os
import re

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    print("❌ Missing BOT_TOKEN")
    exit(1)

bot = telebot.TeleBot(TOKEN)

# /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "🧮 Bot tính toán\n"
        "Gõ phép tính ví dụ:\n"
        "2+3\n10-5\n4*6\n20/4"
    )

# Tính toán
@bot.message_handler(func=lambda m: m.text and re.match(r'^\s*\d+(\.\d+)?\s*[\+\-\*/]\s*\d+(\.\d+)?\s*$', m.text))
def calculate(message):
    try:
        expression = message.text.replace(" ", "")
        result = eval(expression)
        bot.reply_to(message, f"= {result}")
    except ZeroDivisionError:
        bot.reply_to(message, "❌ Không chia cho 0")
    except:
        bot.reply_to(message, "❌ Lỗi phép tính")

print("✅ Bot is running...")
bot.infinity_polling()
