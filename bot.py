import os
import json
import threading
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from google.oauth2.service_account import Credentials
import gspread

# --- Dummy сервер для Render
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

# 🔄 Запускаємо dummy-сервер фоном
threading.Thread(target=run_dummy_server).start()

# 🔐 Логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 🔐 Змінні середовища
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
creds_json = os.getenv("GOOGLE_CREDS")
creds_dict = json.loads(creds_json)

# 🔐 Авторизація Google Sheets з READ-ONLY scopes
scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
google_creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
client = gspread.authorize(google_creds)

# 🧠 Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привіт! Надішли код товару (артикул), і я знайду його у Google Sheets 🔍"
    )

# 🔍 Обробка артикула
async def handle_article(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        logger.error(f"❗ Помилка при запиті до таблиці: {e}")
        await update.message.reply_text(f"⚠️ Помилка: {e}")

# 🚨 Обробка внутрішніх помилок
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(msg="Виникла помилка:", exc_info=context.error)

# 🚀 Запуск бота
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_article))
    app.add_error_handler(error_handler)

    print("🤖 Biom Assistant запущено. Очікую артикул в Telegram...")
    app.run_polling()
