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
