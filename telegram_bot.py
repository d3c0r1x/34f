import logging
import time
from telegram import Bot
from config import config

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_message(message):
    """
    Отправка сообщения в Telegram.
    """
    bot_token = config['telegram']['bot_token']
    chat_id = config['telegram']['chat_id']
    bot = Bot(token=bot_token)
    bot.send_message(chat_id=chat_id, text=message)
    logger.info(f"Сообщение отправлено: {message}")

def monitor_bot_status():
    """
    Мониторинг состояния бота.
    """
    while True:
        logger.info("Мониторинг состояния бота...")
        send_message("Бот работает корректно.")
        time.sleep(config['telegram']['status_interval'])

if __name__ == "__main__":
    monitor_bot_status()