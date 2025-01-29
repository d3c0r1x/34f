import logging
import time
from core import get_exchange_data, get_all_pairs
from config import config

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def measure_performance():
    """
    Измерение производительности бота.
    """
    exchanges = config['exchanges']
    all_pairs = get_all_pairs(exchanges)

    start_time = time.time()

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
                    logger.error(f"Ошибка при измерении производительности биржи {exchange_name}: {e}")

    end_time = time.time()
    duration = end_time - start_time
    logger.info(f"Производительность бота: {duration:.2f} секунд")

def run_performance_analysis():
    """
    Запуск анализа производительности.
    """
    while True:
        logger.info("Запуск анализа производительности...")
        measure_performance()
        logger.info("Анализ производительности завершен.")
        time.sleep(config['performance_interval'])

if __name__ == "__main__":
    run_performance_analysis()