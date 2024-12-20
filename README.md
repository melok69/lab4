# TicketManagerApp

**TicketManagerApp** — это приложение для управления тикетами, созданными пользователями. В нем реализована возможность администратора создавать и управлять тикетами, отправлять сообщения игрокам и взаимодействовать с Telegram-ботом для уведомлений. Оно использует библиотеку **PyQt5** для графического интерфейса и поддерживает работу с базой данных для хранения информации о тикетах и сообщениях.

## Особенности приложения

### 1. Управление тикетами
- **Создание тикетов**: Пользователи могут создавать тикеты, которые регистрируются в системе.
- **Просмотр тикетов**: Администраторы могут просматривать все тикеты в интерфейсе.
- **Отправка сообщений**: Администраторы могут отправлять сообщения в тикеты, как для игроков, так и для себя.
- **Интерфейс управления тикетами**: Графический интерфейс позволяет удобно выбирать тикеты и работать с ними.

### 2. Telegram-уведомления
- При отправке сообщения администратором, оно также отправляется пользователю через **Telegram** по его **ID**.
- Возможность администратора взаимодействовать с пользователями через Telegram, отправляя им уведомления о статусе тикета.

### 3. Поддержка сообщений
- Сообщения отображаются как для администраторов, так и для игроков, обеспечивая двухстороннюю связь.
- Все сообщения о тикетах сохраняются в базе данных для удобного поиска и отслеживания.

## Технические детали

**TicketManagerApp** использует следующую архитектуру:
- **MainWindow**: Основное окно приложения, где отображаются все тикеты и доступ к их созданию.
- **TicketWindow**: Окно для отображения конкретного тикета и сообщений, где администратор может отправлять новые сообщения.
- **Database**: База данных для хранения информации о тикетах и сообщениях.
- **Telegram Bot**: Интеграция с Telegram для отправки сообщений пользователю по ID.

## Установка

1. Убедитесь, что у вас установлен Python версии 3.7 или выше.
2. Установите необходимые зависимости:

   ```bash
   pip install PyQt5 python-telegram-bot
