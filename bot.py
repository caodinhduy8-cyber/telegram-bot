import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    print("❌ Missing BOT_TOKEN")
    exit(1)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🤖 Bot đã hoạt động 24/7 trên Railway!")

@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, f"Bạn gửi: {message.text}")

print("✅ Bot is running...")
bot.infinity_polling()
