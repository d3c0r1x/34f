import logging
import unittest
from core import get_exchange_data, place_order, get_all_pairs
from config import config

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestBotFunctions(unittest.TestCase):
    def setUp(self):
        self.exchanges = config['exchanges']
        self.all_pairs = get_all_pairs(self.exchanges)

    def test_get_exchange_data(self):
        for exchange_name, exchange_config in self.exchanges.items():
            for pair in self.all_pairs:
                for account in exchange_config['accounts']:
                    with self.subTest(exchange=exchange_name, pair=pair, account=account):
                        data = get_exchange_data(exchange_name, pair, account)
                        self.assertIsNotNone(data)
                        self.assertIn('buy_price', data)
                        self.assertIn('sell_price', data)

    def test_place_order(self):
        for exchange_name, exchange_config in self.exchanges.items():
            for pair in self.all_pairs:
                for account in exchange_config['accounts']:
                    with self.subTest(exchange=exchange_name, pair=pair, account=account):
                        data = get_exchange_data(exchange_name, pair, account)
                        if data:
                            buy_price = data['buy_price']
                            sell_price = data['sell_price']
                            if buy_price and sell_price:
                                trade_amount = Decimal(config['trade_amount'])
                                buy_order_id = place_order(exchange_name, pair, 'buy', trade_amount, buy_price, account)
                                self.assertIsNotNone(buy_order_id)
                                sell_order_id = place_order(exchange_name, pair, 'sell', trade_amount, sell_price, account)
                                self.assertIsNotNone(sell_order_id)

def run_tests():
    """
    Запуск юнит-тестов.
    """
    logger.info("Запуск юнит-тестов...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBotFunctions)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    if result.wasSuccessful():
        logger.info("Все тесты прошли успешно.")
    else:
        logger.error("Некоторые тесты не прошли.")

if __name__ == "__main__":
    run_tests()