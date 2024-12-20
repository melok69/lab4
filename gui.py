import asyncio
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QTextEdit, QWidget, QLineEdit, QMessageBox, QDialog, QFormLayout
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import database
import telegram_bot


class TelegramWorker(QThread):
    """Поток для отправки сообщений в Telegram."""
    message_sent = pyqtSignal(str)

    def __init__(self, ticket_id, reply_text):
        super().__init__()
        self.ticket_id = ticket_id
        self.reply_text = reply_text

    def run(self):
        # Асинхронная отправка сообщения в Telegram
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(telegram_bot.send_to_admin(f"Admin replied to ticket {self.ticket_id}: {self.reply_text}"))
        loop.close()
        self.message_sent.emit(f"Admin replied to ticket {self.ticket_id}: {self.reply_text}")


class TicketWindow(QDialog):  # Меняем QMainWindow на QDialog
    def __init__(self, ticket_id, messages, parent=None):
        super().__init__(parent)

        self.ticket_id = ticket_id
        self.messages = messages
        self.setWindowTitle(f"Ticket #{ticket_id}")
        self.setGeometry(100, 100, 600, 400)

        # Область чата
        self.chat_area = QTextEdit(self)
        self.chat_area.setReadOnly(True)

        # Ввод сообщения
        self.message_input = QLineEdit(self)

        # Кнопка отправки
        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_message)

        # Размещение элементов
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Messages for Ticket #{ticket_id}"))
        layout.addWidget(self.chat_area)
        layout.addWidget(self.message_input)
        layout.addWidget(self.send_button)
        self.setLayout(layout)

        # Отображение сообщений
        self.display_messages()

    def display_messages(self):
        """Отображение сообщений в chat_area"""
        for message in self.messages:
            if len(message) == 2:  # Если сообщений только два, добавляем фейковый идентификатор
                message = ('Unknown ID', message[0], message[1])  # Добавляем идентификатор
            elif len(message) != 3:
                print(f"Invalid message format: {message}")
                continue
            self.chat_area.append(f"{message[1]}: {message[2]}")  # message[1] - имя, message[2] - текст сообщения

    def send_message(self):
        """Обработка отправки сообщения"""
        message = self.message_input.text()
        if message:
            # Добавляем сообщение с нужным форматом
            self.messages.append(('admin', message))  # Пример добавления сообщения от админа
            self.display_messages()
            self.message_input.clear()

class AdminApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Panel - Support Tickets")
        self.setGeometry(100, 100, 800, 600)

        # Основной виджет и макет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Таблица обращений
        self.tickets_table = QTableWidget(self)
        self.tickets_table.setColumnCount(2)
        self.tickets_table.setHorizontalHeaderLabels(["ID", "User"])
        self.tickets_table.cellDoubleClicked.connect(self.open_ticket)
        self.layout.addWidget(self.tickets_table)

        # Кнопки управления
        self.refresh_button = QPushButton("Обновить список", self)
        self.refresh_button.clicked.connect(self.load_tickets)
        self.layout.addWidget(self.refresh_button)

        # Загрузка данных при запуске
        self.current_ticket_id = None
        self.load_tickets()

    def load_tickets(self):
        """Загружает список обращений из базы данных."""
        self.tickets_table.setRowCount(0)
        tickets = database.get_all_tickets()
        for row, ticket in enumerate(tickets):
            self.tickets_table.insertRow(row)
            self.tickets_table.setItem(row, 0, QTableWidgetItem(str(ticket[0])))  # ticket[0] - ID
            self.tickets_table.setItem(row, 1, QTableWidgetItem(ticket[1]))  # ticket[1] - Пользователь

    def open_ticket(self, row, column):
        """Открывает выбранное обращение для ответа."""
        ticket_id = int(self.tickets_table.item(row, 0).text())
        user = self.tickets_table.item(row, 1).text()


        messages = database.get_ticket_messages(ticket_id)
        self.ticket_window = TicketWindow(ticket_id, messages, self)
        self.ticket_window.exec()

    def send_reply(self):
        """Отправка ответа на тикет."""
        if self.current_ticket_id is None:
            QMessageBox.warning(self, "Ошибка", "Выберите обращение для ответа.")
            return

        reply_text = self.reply_input.text().strip()
        if not reply_text:
            QMessageBox.warning(self, "Ошибка", "Текст ответа не может быть пустым.")
            return

        database.add_message(self.current_ticket_id, "Admin", reply_text)
        self.chat_area.append(f"Admin: {reply_text}")
        self.reply_input.clear()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    admin_app = AdminApp()
    admin_app.show()
    sys.exit(app.exec())
