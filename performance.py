import time
import logging
from arbitrage import Arbitrage

class Performance:
    def __init__(self, arbitrage):
        self.arbitrage = arbitrage
        self.logger = logging.getLogger('Performance')
        logging.basicConfig(level=logging.INFO)

    def analyze_performance(self):
        while True:
            try:
                performance_data = self.arbitrage.get_performance_data()
                self.evaluate_performance(performance_data)
                self.log_performance(performance_data)
            except Exception as e:
                self.logger.error(f"Error in performance analysis: {e}")
            time.sleep(config['performance_interval'])  # Проверять каждые 3600 секунд

    def evaluate_performance(self, performance_data):
        # Логика оценки производительности
        if performance_data['success_rate'] < 0.8:
            self.logger.warning("Low success rate detected")
        else:
            self.logger.info("Performance is satisfactory")

    def log_performance(self, performance_data):
        self.logger.info(f"Performance data: {performance_data}")

if __name__ == "__main__":
    arbitrage = Arbitrage()
    performance = Performance(arbitrage)
    performance.analyze_performance()
