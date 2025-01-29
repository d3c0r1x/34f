import logging
import time
from core import get_exchange_data, get_all_pairs
from config import config

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def monitor_exchanges():
    """
    Мониторинг состояния бирж.
    """
    exchanges = config['exchanges']
    all_pairs = get_all_pairs(exchanges)

    for exchange_name, exchange_config in exchanges.items():
        for pair in all_pairs:
            for account in exchange_config['accounts']:
                try:
                    exchange_data = get_exchange_data(exchange_name, pair, account)
                    if not exchange_data:
                        logger.warning(f"Нет данных для биржи {exchange_name} и пары {pair}")
                        continue

                    buy_price = exchange_data.get('buy_price', 0)
                    sell_price = exchange_data.get('sell_price', 0)

                    if not buy_price or not sell_price:
                        logger.warning(f"Нет данных о ценах для биржи {exchange_name} и пары {pair}")

                except Exception as e:
                    logger.error(f"Ошибка при мониторинге биржи {exchange_name}: {e}")

def run_monitoring():
    """
    Запуск мониторинга.
    """
    while True:
        logger.info("Запуск мониторинга бирж...")
        monitor_exchanges()
        logger.info("Мониторинг бирж завершен.")
        time.sleep(config['monitoring_interval'])

if __name__ == "__main__":
    run_monitoring()