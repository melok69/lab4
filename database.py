import sqlite3

# Инициализация базы данных
def initialize_database():
    conn = sqlite3.connect('support_tickets.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tickets
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user TEXT,
                  is_closed BOOLEAN DEFAULT FALSE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  ticket_id INTEGER,
                  sender TEXT,
                  message TEXT,
                  FOREIGN KEY(ticket_id) REFERENCES tickets(id))''')
    conn.commit()
    conn.close()

# Получение всех тикетов
def get_all_tickets():
    conn = sqlite3.connect('support_tickets.db')
    c = conn.cursor()
    c.execute("SELECT id, user, is_closed FROM tickets")
    tickets = c.fetchall()
    conn.close()
    return tickets

# Получение сообщений для тикета
def get_ticket_messages(ticket_id):
    conn = sqlite3.connect('support_tickets.db')
    c = conn.cursor()
    c.execute("SELECT sender, message FROM messages WHERE ticket_id = ?", (ticket_id,))
    messages = c.fetchall()
    conn.close()
    return messages

# Добавление тикета
def add_ticket(user, question):
    conn = sqlite3.connect('support_tickets.db')
    c = conn.cursor()
    c.execute("INSERT INTO tickets (user, is_closed) VALUES (?, ?)", (user, False))
    ticket_id = c.lastrowid
    c.execute("INSERT INTO messages (ticket_id, sender, message) VALUES (?, ?, ?)", (ticket_id, user, question))
    conn.commit()
    conn.close()

# Закрытие тикета
def close_ticket(ticket_id):
    conn = sqlite3.connect('support_tickets.db')
    c = conn.cursor()
    c.execute("UPDATE tickets SET is_closed = ? WHERE id = ?", (True, ticket_id))
    conn.commit()
    conn.close()

# Добавление сообщения в тикет
def add_message(ticket_id, sender, message):
    conn = sqlite3.connect('support_tickets.db')
    c = conn.cursor()
    c.execute("INSERT INTO messages (ticket_id, sender, message) VALUES (?, ?, ?)", (ticket_id, sender, message))
    conn.commit()
    conn.close()