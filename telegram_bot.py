import logging
import time
import telebot

class TelegramBot:
    def __init__(self):
        self.bot = telebot.TeleBot(config['telegram']['bot_token'])
        self.chat_id = config['telegram']['chat_id']
        self.logger = logging.getLogger('TelegramBot')
        logging.basicConfig(level=logging.INFO)

    def send_status(self):
        while True:
            try:
                status_message = "Bot is running and monitoring market conditions."
                self.bot.send_message(self.chat_id, status_message)
                self.logger.info("Status message sent to Telegram")
            except Exception as e:
                self.logger.error(f"Error sending status message: {e}")
            time.sleep(config['telegram']['status_interval'])  # Отправлять статус каждые 3600 секунд

if __name__ == "__main__":
    telegram_bot = TelegramBot()
    telegram_bot.send_status()
