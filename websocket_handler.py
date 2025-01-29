import time
import logging
import websocket
import json

class WebSocketHandler:
    def __init__(self):
        self.ws = None
        self.market_data = {}
        self.logger = logging.getLogger('WebSocketHandler')
        logging.basicConfig(level=logging.INFO)

    def run(self):
        for exchange_name, exchange_config in config['exchanges'].items():
            self.ws = websocket.WebSocketApp(exchange_config['websocket_uri'],
                                            on_message=self.on_message,
                                            on_error=self.on_error,
                                            on_close=self.on_close)
            self.logger.info(f"WebSocket started for {exchange_name}")
            self.ws.run_forever()

    def on_message(self, ws, message):
        try:
            data = json.loads(message)
            self.market_data.update(data)
            self.logger.info(f"Received market data: {data}")
        except Exception as e:
            self.logger.error(f"Error parsing message: {e}")

    def on_error(self, ws, error):
        self.logger.error(f"WebSocket error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        self.logger.info("WebSocket closed")

    def get_market_data(self):
        return self.market_data

    def execute_trade(self, trade):
        # Логика выполнения сделки
        self.logger.info(f"Executing trade: {trade}")

if __name__ == "__main__":
    websocket_handler = WebSocketHandler()
    websocket_handler.run()
