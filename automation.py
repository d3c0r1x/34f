import time
import threading
from websocket_handler import WebSocketHandler
from arbitrage import Arbitrage
from ml_model import MLModel
from profit_optimizer import ProfitOptimizer
from security import Security
from log_analysis import LogAnalysis
from performance import Performance
from monitoring import Monitoring
from telegram_bot import TelegramBot

class Automation:
    def __init__(self):
        self.websocket_handler = WebSocketHandler()
        self.arbitrage = Arbitrage(self.websocket_handler)
        self.ml_model = MLModel()
        self.profit_optimizer = ProfitOptimizer()
        self.security = Security()
        self.log_analysis = LogAnalysis()
        self.performance = Performance(self.arbitrage)
        self.monitoring = Monitoring(self.websocket_handler)
        self.telegram_bot = TelegramBot()

    def start_automation(self):
        self.start_websocket()
        self.start_arbitrage()
        self.start_ml_training()
        self.start_profit_optimization()
        self.start_security_monitoring()
        self.start_log_analysis()
        self.start_performance_analysis()
        self.start_market_monitoring()
        self.start_telegram_notifications()

    def start_websocket(self):
        threading.Thread(target=self.websocket_handler.run, daemon=True).start()

    def start_arbitrage(self):
        threading.Thread(target=self.arbitrage.run, daemon=True).start()

    def start_ml_training(self):
        threading.Thread(target=self.ml_model.train, daemon=True).start()

    def start_profit_optimization(self):
        threading.Thread(target=self.profit_optimizer.optimize, daemon=True).start()

    def start_security_monitoring(self):
        threading.Thread(target=self.security.monitor, daemon=True).start()

    def start_log_analysis(self):
        threading.Thread(target=self.log_analysis.analyze_logs, daemon=True).start()

    def start_performance_analysis(self):
        threading.Thread(target=self.performance.analyze_performance, daemon=True).start()

    def start_market_monitoring(self):
        threading.Thread(target=self.monitoring.monitor, daemon=True).start()

    def start_telegram_notifications(self):
        threading.Thread(target=self.telegram_bot.send_status, daemon=True).start()

if __name__ == "__main__":
    automation = Automation()
    automation.start_automation()
    while True:
        time.sleep(config['automation_interval'])
