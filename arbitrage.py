import logging
import time
from decimal import Decimal
from config import config
from core import get_exchange_data, place_order, get_all_pairs
from analytics import get_historical_data, calculate_indicators, analyze_liquidity, fetch_additional_data, generate_report
from ml_model import MLModel
from profit_optimizer import ProfitOptimizer
from websocket_handler import WebSocketHandler

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Arbitrage:
    def __init__(self, websocket_handler):
        self.websocket_handler = websocket_handler
        self.ml_model = MLModel()
        self.profit_optimizer = ProfitOptimizer()
        self.logger = logging.getLogger('Arbitrage')
        logging.basicConfig(level=logging.INFO)

    def run(self):
        while True:
            try:
                self.find_arbitrage_opportunities()
            except Exception as e:
                self.logger.error(f"Error in arbitrage: {e}")
            time.sleep(config['check_interval'])

    def find_arbitrage_opportunities(self):
        """
        Поиск арбитражных возможностей между биржами.
        """
        exchanges = config['exchanges']
        all_pairs = get_all_pairs(exchanges)
        min_profit_margin = Decimal(config['min_profit_margin'])
        for pair in all_pairs:
            logger.info(f"Ищу арбитражные возможности для пары {pair}")
            best_buy_price = None
            best_sell_price = None
            best_buy_exchange = None
            best_sell_exchange = None
            best_buy_account = None
            best_sell_account = None
            # Получение исторических данных и аналитики
            historical_data = get_historical_data(pair)
            historical_data = calculate_indicators(historical_data)
            historical_data = analyze_liquidity(historical_data)
            additional_data = fetch_additional_data(pair)
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
                        logger.error(f"Ошибка при получении данных с биржи {exchange_name}: {e}")
            if best_buy_exchange and best_sell_exchange:
                profit_margin = (best_sell_price - best_buy_price) / best_buy_price * 100
                if profit_margin >= min_profit_margin:
                    logger.info(f"Найдена арбитражная возможность для пары {pair}:")
                    logger.info(f"Покупка на {best_buy_exchange} по цене {best_buy_price} с аккаунтом {best_buy_account}")
                    logger.info(f"Продажа на {best_sell_exchange} по цене {best_sell_price} с аккаунтом {best_sell_account}")
                    logger.info(f"Маржа: {profit_margin:.2f}%")
                    # Проверяем доступность средств и объема для торговли
                    available_funds = Decimal(config['available_funds'])
                    max_trade_amount = Decimal(config['max_trade_amount'])
                    trade_amount = min(max_trade_amount, available_funds / best_buy_price)
                    if available_funds >= best_buy_price * trade_amount:
                        try:
                            # Покупаем на лучшей бирже покупки
                            buy_order_id = place_order(best_buy_exchange, pair, 'buy', trade_amount, best_buy_price, best_buy_account)
                            logger.info(f"Выполнена покупка на {best_buy_exchange}, ордер ID: {buy_order_id}")
                            # Продаем на лучшей бирже продажи
                            sell_order_id = place_order(best_sell_exchange, pair, 'sell', trade_amount, best_sell_price, best_sell_account)
                            logger.info(f"Выполнена продажа на {best_sell_exchange}, ордер ID: {sell_order_id}")
                            # Установка стоп-лоссов и тейк-профитов
                            stop_loss = best_buy_price * (1 - Decimal(config['stop_loss_percentage']))
                            take_profit = best_buy_price * (1 + Decimal(config['take_profit_percentage']))
                            logger.info(f"Стоп-лосс: {stop_loss}, Тейк-профит: {take_profit}")
                            # Обновляем доступные средства
                            available_funds -= best_buy_price * trade_amount
                            config['available_funds'] = available_funds
                        except Exception as e:
                            logger.error(f"Ошибка при выполнении арбитражной сделки: {e}")
                    else:
                        logger.warning(f"Недостаточно средств для торговли парой {pair}")
                else:
                    logger.info(f"Арбитражная возможность для пары {pair} не найдена (маржа: {profit_margin:.2f}%)")
            else:
                logger.warning(f"Не удалось найти подходящие цены для пары {pair}")

if __name__ == "__main__":
    websocket_handler = WebSocketHandler()
    arbitrage = Arbitrage(websocket_handler)
    arbitrage.run()
