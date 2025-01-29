import logging
import asyncio
import websockets
from config import config

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def handle_websocket(uri, pair, account):
    """
    Обработка подключения к WebSocket.
    """
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            logger.info(f"Получено сообщение: {message}")
            # Обработка сообщения и обновление данных

def start_websocket_listener(exchange_name, pair, account):
    """
    Запуск WebSocket-слушателя для биржи.
    """
    uri = config['exchanges'][exchange_name].get('websocket_uri')
    if not uri:
        logger.warning(f"WebSocket URI не указан для биржи {exchange_name}")
        return

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(handle_websocket(uri, pair, account))

def run_websocket_listeners():
    """
    Запуск всех WebSocket-слушателей.
    """
    exchanges = config['exchanges']
    all_pairs = get_all_pairs(exchanges)

    for exchange_name, exchange_config in exchanges.items():
        for pair in all_pairs:
            for account in exchange_config['accounts']:
                listener_thread = Thread(target=start_websocket_listener, args=(exchange_name, pair, account))
                listener_thread.daemon = True
                listener_thread.start()

if __name__ == "__main__":
    run_websocket_listeners()