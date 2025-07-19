<<<<<<< HEAD
import os
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from google.oauth2.service_account import Credentials
import gspread

# --- Dummy сервер для Render (імітація порту)
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Biom Assistant is alive.")

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Dummy сервер запускається на порту {port}...")
    server = HTTPServer(("", port), DummyHandler)
    server.serve_forever()

# Запускаємо фоновий dummy-сервер
threading.Thread(target=run_dummy_server).start()

# --- Telegram Token (змінна середовища)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# --- Авторизація до Google Sheets через GOOGLE_CREDS
creds_json = os.getenv("GOOGLE_CREDS")
creds_dict = json.loads(creds_json)
google_creds = Credentials.from_service_account_info(creds_dict)
client = gspread.authorize(google_creds)

# --- Обробка /start
async def start(update, context):
    await update.message.reply_text(
        "👋 Привіт! Надішли код товару (артикул), і я знайду його у Google Sheets 🔍"
    )

# --- Обробка звичайного тексту (код товару)
async def handle_article(update, context):
    code = update.message.text.strip()

    if not code.isdigit():
        await update.message.reply_text("❌ Введи лише числовий артикул.")
        return

    try:
        sheet = client.open("Biom BOT").sheet1
        records = sheet.get_all_records()

        match = next((r for r in records if str(r.get("Код")).strip() == code), None)

        if match:
            name = match.get("Назва", "Невідомо")
            price = match.get("Ціна", "—")
            stock = match.get("Наявність", "—")
            await update.message.reply_text(
                f"📦 Назва: {name}\n💰 Ціна: {price} грн\n📍 Наявність: {stock}"
            )
        else:
            await update.message.reply_text("😕 Код не знайдено в таблиці.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Помилка: {e}")

# --- Запуск Telegram‑бота
app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_article))

print("🤖 Biom Assistant запущено. Очікую артикул в Telegram...")
app.run_polling()
=======
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 🔐 Твій токен — не забудь винести в .env для хмарного хостингу!
TOKEN = '7875054563:AAFgt4bTm3VXg2ZyEaslXjNZGIUsPUJ0lMY'

# 📝 Налаштування логів — допомагає бачити помилки
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# 📌 Обробник команди /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я бот Biom Assistant. Готовий відповісти на твої запити 🧠")

# 📌 Обробник звичайних повідомлень
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"Ти написав: {text}")

# 📌 Обробник помилок
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(msg="Виникла помилка:", exc_info=context.error)

# 🚀 Запуск бота
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    print("✅ Бот запущено — очікуємо повідомлення...")
    app.run_polling()
>>>>>>> d1c30b92bdbd730b3ee9121850589f220efd7c40
