import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8276187019:AAG55zc3_cj8VatEyp0453K-CLq1Goqpqhk"

def get_usdt_price():
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    payload = {
        "page": 1,
        "rows": 5,
        "asset": "USDT",
        "fiat": "VND",
        "tradeType": "BUY"
    }
    r = requests.post(url, json=payload, timeout=10).json()
    return r["data"][0]["adv"]["price"]

async def usdt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = get_usdt_price()
    await update.message.reply_text(
        f"💵 Giá USDT/VND (Binance P2P)\n👉 {price} VND"
    )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text.lower() in ["usdt", "giá usdt"]:
        await usdt(update, context)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("usdt", usdt))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

print("Bot USDT dang chay...")
app.run_polling()
