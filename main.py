import sys
from multiprocessing import Process
from PyQt5.QtWidgets import QApplication
from gui import AdminApp
import database
from telegram_bot import start_telegram_bot


def run_telegram_bot():
    # Запуск Telegram-бота в отдельном процессе
    start_telegram_bot()


def main():
    # Инициализация базы данных
    database.initialize_database()

    # Запуск Telegram-бота в отдельном процессе
    bot_process = Process(target=run_telegram_bot)
    bot_process.start()

    # Запуск графического интерфейса
    app = QApplication(sys.argv)
    admin_app = AdminApp()
    admin_app.show()
    app.exec()

    # Остановка процесса Telegram-бота при завершении GUI
    bot_process.terminate()
    bot_process.join()


if __name__ == "__main__":
    main()
