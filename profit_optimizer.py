import logging
from core import get_exchange_data, get_all_pairs
from config import config

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def optimize_trade_amount(pair, buy_price, sell_price, available_funds):
    """
    Оптимизация объема торговли для пары.
    """
    max_trade_amount = available_funds / buy_price
    optimal_trade_amount = min(max_trade_amount, Decimal(config['max_trade_amount']))

    return optimal_trade_amount

def optimize_profit(pair, buy_price, sell_price, available_funds):
    """
    Оптимизация прибыли для пары.
    """
    profit_margin = (sell_price - buy_price) / buy_price * 100

    if profit_margin >= Decimal(config['min_profit_margin']):
        trade_amount = optimize_trade_amount(pair, buy_price, sell_price, available_funds)
        return trade_amount, profit_margin
    else:
        return None, None

def run_profit_optimization():
    """
    Запуск оптимизации прибыли.
    """
    exchanges = config['exchanges']
    all_pairs = get_all_pairs(exchanges)
    available_funds = Decimal(config['available_funds'])

    for pair in all_pairs:
        logger.info(f"Оптимизация прибыли для пары {pair}")

        best_buy_price = None
        best_sell_price = None
        best_buy_exchange = None
        best_sell_exchange = None
        best_buy_account = None
        best_sell_account = None

        for exchange_name, exchange_config in exchanges.items():
            for account in exchange_config['accounts']:
                try:
                    exchange_data = get_exchange_data(exchange_name, pair, account)
                    if not exchange_data:
                        logger.warning(f"Нет данных для биржи {exchange_name} и пары {pair}")
                        continue

                    buy_price = Decimal(exchange_data.get('buy_price', 0))
                    sell_price = Decimal(exchange_data.get('sell_price', 0))

                    if best_buy_price is None or buy_price < best_buy_price:
                        best_buy_price = buy_price
                        best_buy_exchange = exchange_name
                        best_buy_account = account

                    if best_sell_price is None or sell_price > best_sell_price:
                        best_sell_price = sell_price
                        best_sell_exchange = exchange_name
                        best_sell_account = account

                except Exception as e:
                    logger.error(f"Ошибка при оптимизации прибыли на бирже {exchange_name}: {e}")

        if best_buy_exchange and best_sell_exchange:
            trade_amount, profit_margin = optimize_profit(pair, best_buy_price, best_sell_price, available_funds)
            if trade_amount and profit_margin:
                logger.info(f"Оптимальный объем торговли для пары {pair}: {trade_amount}")
                logger.info(f"Оптимальная маржа: {profit_margin:.2f}%")
            else:
                logger.info(f"Нет оптимальных условий для пары {pair}")

if __name__ == "__main__":
    run_profit_optimization()