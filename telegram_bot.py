#7814228020:AAEURRRaOSinAJJteIMYD3ouy53mzqV8MDI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram import Bot

import database

# Ваш токен бота
TOKEN = "7814228020:AAEURRRaOSinAJJteIMYD3ouy53mzqV8MDI"
ADMIN_CHAT_ID = "726480962"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the Support Bot! Please type your question.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.username or "Anonymous"
    question = update.message.text
    # Добавляем тикет в базу данных
    database.add_ticket(user_name, question)
    
    # Отправляем ответ в Telegram
    await update.message.reply_text("Thank you! Your question has been received.")

    # Отправка уведомления администратору
    await send_to_admin(f"New ticket from {user_name}: {question}")

async def send_to_admin(message):
    # Создаем объект Bot для отправки сообщения
    bot = Bot(token=TOKEN)
    # Используем await для асинхронного вызова
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=message)

def start_telegram_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()
