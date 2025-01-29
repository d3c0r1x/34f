import logging
import time
from core import get_exchange_data, place_order, get_all_pairs
from config import config

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def simulate_trades():
    """
    Симуляция торговли для нагрузочного тестирования.
    """
    exchanges = config['exchanges']
    all_pairs = get_all_pairs(exchanges)

    for pair in all_pairs:
        logger.info(f"Симуляция торговли для пары {pair}")

        for exchange_name, exchange_config in exchanges.items():
            for account in exchange_config['accounts']:
                try:
                    exchange_data = get_exchange_data(exchange_name, pair, account)
                    if not exchange_data:
                        logger.warning(f"Нет данных для биржи {exchange_name} и пары {pair}")
                        continue

                    buy_price = exchange_data.get('buy_price', 0)
                    sell_price = exchange_data.get('sell_price', 0)

                    if buy_price and sell_price:
                        trade_amount = Decimal(config['trade_amount'])

                        # Покупаем на лучшей бирже покупки
                        buy_order_id = place_order(exchange_name, pair, 'buy', trade_amount, buy_price, account)
                        logger.info(f"Симулирована покупка на {exchange_name}, ордер ID: {buy_order_id}")

                        # Продаем на лучшей бирже продажи
                        sell_order_id = place_order(exchange_name, pair, 'sell', trade_amount, sell_price, account)
                        logger.info(f"Симулирована продажа на {exchange_name}, ордер ID: {sell_order_id}")

                except Exception as e:
                    logger.error(f"Ошибка при симуляции торговли на бирже {exchange_name}: {e}")

def run_load_test():
    """
    Запуск нагрузочного тестирования.
    """
    start_time = time.time()
    simulate_trades()
    end_time = time.time()
    duration = end_time - start_time
    logger.info(f"Нагрузочное тестирование завершено. Время выполнения: {duration:.2f} секунд")

if __name__ == "__main__":
    run_load_test()