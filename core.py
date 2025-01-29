import logging
import requests
from config import config

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_exchange_data(exchange_name, pair, account):
    """
    Получение данных о ценах с биржи.
    """
    try:
        if exchange_name == 'okx':
            url = f"https://www.okx.com/api/v5/market/ticker?instId={pair.replace('/', '-')}"
            response = requests.get(url)
            data = response.json()['data'][0]
            return {
                'buy_price': Decimal(data['bidPx']),
                'sell_price': Decimal(data['askPx'])
            }
        elif exchange_name == 'bybit':
            url = f"https://api.bybit.com/v2/public/tickers?symbol={pair.replace('/', '')}"
            response = requests.get(url)
            data = response.json()['result'][0]
            return {
                'buy_price': Decimal(data['bid_price']),
                'sell_price': Decimal(data['ask_price'])
            }
        elif exchange_name == 'huobi':
            url = f"https://api.huobi.pro/market/detail/merged?symbol={pair.replace('/', '').lower()}"
            response = requests.get(url)
            data = response.json()['tick']
            return {
                'buy_price': Decimal(data['bid'][0]),
                'sell_price': Decimal(data['ask'][0])
            }
        elif exchange_name == 'bitget':
            url = f"https://api.bitget.com/api/mix/v1/market/ticker?symbol={pair.replace('/', '_')}_UMCBL"
            response = requests.get(url)
            data = response.json()['data'][0]
            return {
                'buy_price': Decimal(data['bestAsk1']),
                'sell_price': Decimal(data['bestBid1'])
            }
        elif exchange_name == 'ftx':
            url = f"https://ftx.com/api/markets/{pair.replace('/', '-')}/orderbook?depth=1"
            response = requests.get(url)
            data = response.json()['result']
            return {
                'buy_price': Decimal(data['bids'][0][0]),
                'sell_price': Decimal(data['asks'][0][0])
            }
        elif exchange_name == 'deribit':
            url = f"https://www.deribit.com/api/v2/public/get_order_book?instrument_name={pair.replace('/', '-')}-PERPETUAL"
            response = requests.get(url)
            data = response.json()['result']
            return {
                'buy_price': Decimal(data['bids'][0][0]),
                'sell_price': Decimal(data['asks'][0][0])
            }
        elif exchange_name == 'gateio':
            url = f"https://api.gateio.ws/api/v4/futures/order_book?contract={pair.replace('/', '_')}_USDT"
            response = requests.get(url)
            data = response.json()
            return {
                'buy_price': Decimal(data['bids'][0][0]),
                'sell_price': Decimal(data['asks'][0][0])
            }
        else:
            logger.error(f"Неизвестная биржа: {exchange_name}")
            return None
    except Exception as e:
        logger.error(f"Ошибка при получении данных с биржи {exchange_name}: {e}")
        return None

def place_order(exchange_name, pair, order_type, amount, price, account):
    """
    Выполнение торгового ордера на бирже.
    """
    try:
        if exchange_name == 'okx':
            url = "https://www.okx.com/api/v5/trade/order"
            headers = {
                'OK-ACCESS-KEY': account['api_key'],
                'OK-ACCESS-SIGN': 'SIGNATURE',  # Замените на реальное значение
                'OK-ACCESS-TIMESTAMP': 'TIMESTAMP',  # Замените на реальное значение
                'OK-ACCESS-PASSPHRASE': account['passphrase']
            }
            data = {
                'instId': pair.replace('/', '-'),
                'tdMode': 'cash',
                'side': 'buy' if order_type == 'buy' else 'sell',
                'ordType': 'limit',
                'sz': str(amount),
                'px': str(price)
            }
            response = requests.post(url, headers=headers, json=data)
            data = response.json()
            return data['data'][0]['ordId']
        elif exchange_name == 'bybit':
            url = "https://api.bybit.com/v2/private/order/create"
            headers = {
                'api-key': account['api_key'],
                'sign': 'SIGNATURE'  # Замените на реальное значение
            }
            params = {
                'symbol': pair.replace('/', ''),
                'side': 'Buy' if order_type == 'buy' else 'Sell',
                'order_type': 'Limit',
                'qty': str(amount),
                'price': str(price),
                'time_in_force': 'GoodTillCancel'
            }
            response = requests.post(url, headers=headers, params=params)
            data = response.json()
            return data['result']['order_id']
        elif exchange_name == 'huobi':
            url = "https://api.huobi.pro/v1/order/orders/place"
            headers = {
                'Content-Type': 'application/json',
                'AccessKeyId': account['api_key'],
                'SignatureMethod': 'HmacSHA256',
                'SignatureVersion': '2',
                'Timestamp': 'TIMESTAMP',  # Замените на реальное значение
                'Signature': 'SIGNATURE'  # Замените на реальное значение
            }
            data = {
                'account-id': 'ACCOUNT_ID',  # Замените на реальное значение
                'symbol': pair.replace('/', '').lower(),
                'type': 'buy-limit' if order_type == 'buy' else 'sell-limit',
                'amount': str(amount),
                'price': str(price)
            }
            response = requests.post(url, headers=headers, json=data)
            data = response.json()
            return data['data']
        elif exchange_name == 'bitget':
            url = "https://api.bitget.com/api/mix/v1/order/placeOrder"
            headers = {
                'ACCESS-KEY': account['api_key'],
                'ACCESS-SIGN': 'SIGNATURE',  # Замените на реальное значение
                'ACCESS-TIMESTAMP': 'TIMESTAMP',  # Замените на реальное значение
                'ACCESS-PASSPHRASE': account['passphrase']
            }
            data = {
                'symbol': pair.replace('/', '_') + '_UMCBL',
                'marginCoin': 'USDT',
                'orderType': 'limit',
                'side': 'open_long' if order_type == 'buy' else 'open_short',
                'size': str(amount),
                'price': str(price),
                'clientOid': str(time.time())
            }
            response = requests.post(url, headers=headers, json=data)
            data = response.json()
            return data['data']['orderId']
        elif exchange_name == 'ftx':
            url = "https://ftx.com/api/orders"
            headers = {
                'FTX-KEY': account['api_key'],
                'FTX-SIGN': 'SIGNATURE',  # Замените на реальное значение
                'FTX-TS': 'TIMESTAMP'  # Замените на реальное значение
            }
            data = {
                'market': pair.replace('/', '-'),
                'side': 'buy' if order_type == 'buy' else 'sell',
                'price': str(price),
                'type': 'limit',
                'size': str(amount),
                'reduceOnly': False,
                'ioc': False,
                'postOnly': False
            }
            response = requests.post(url, headers=headers, json=data)
            data = response.json()
            return data['result']['id']
        elif exchange_name == 'deribit':
            url = "https://www.deribit.com/api/v2/private/create_order"
            headers = {
                'Authorization': f"Bearer {account['api_key']}"
            }
            data = {
                'instrument_name': pair.replace('/', '-') + '-PERPETUAL',
                'amount': str(amount),
                'price': str(price),
                'type': 'limit',
                'side': 'buy' if order_type == 'buy' else 'sell',
                'time_in_force': 'gtc'
            }
            response = requests.post(url, headers=headers, json=data)
            data = response.json()
            return data['result']['order_id']
        elif exchange_name == 'gateio':
            url = "https://api.gateio.ws/api/v4/futures/orders"
            headers = {
                'Content-Type': 'application/json',
                'Key': account['api_key'],
                'Sign': 'SIGNATURE',  # Замените на реальное значение
                'Timestamp': 'TIMESTAMP'  # Замените на реальное значение
            }
            data = {
                'contract': pair.replace('/', '_') + '_USDT',
                'size': str(amount),
                'price': str(price),
                'side': 'buy' if order_type == 'buy' else 'sell',
                'type': 'limit',
                'tif': 'gtc'
            }
            response = requests.post(url, headers=headers, json=data)
            data = response.json()
            return data['id']
        else:
            logger.error(f"Неизвестная биржа: {exchange_name}")
            return None
    except Exception as e:
        logger.error(f"Ошибка при выполнении ордера на бирже {exchange_name}: {e}")
        return None

def get_all_pairs(exchanges):
    """
    Получение всех торговых пар с всех бирж.
    """
    all_pairs = set()
    for exchange_name, exchange_config in exchanges.items():
        try:
            if exchange_name == 'okx':
                url = "https://www.okx.com/api/v5/public/instruments?instType=SPOT"
                response = requests.get(url)
                data = response.json()
                for instrument in data['data']:
                    pair = f"{instrument['baseCcy']}/{instrument['quoteCcy']}"
                    all_pairs.add(pair)
            elif exchange_name == 'bybit':
                url = "https://api.bybit.com/v2/public/symbols"
                response = requests.get(url)
                data = response.json()
                for symbol in data['result']:
                    pair = f"{symbol['base_currency']}/{symbol['quote_currency']}"
                    all_pairs.add(pair)
            elif exchange_name == 'huobi':
                url = "https://api.huobi.pro/v1/common/symbols"
                response = requests.get(url)
                data = response.json()
                for symbol in data['data']:
                    pair = f"{symbol['base-currency']}/{symbol['quote-currency']}"
                    all_pairs.add(pair)
            elif exchange_name == 'bitget':
                url = "https://api.bitget.com/api/mix/v1/market/products?productType=UMCBL"
                response = requests.get(url)
                data = response.json()
                for product in data['data']:
                    pair = f"{product['symbol'].split('_')[0]}/{product['symbol'].split('_')[1]}"
                    all_pairs.add(pair)
            elif exchange_name == 'ftx':
                url = "https://ftx.com/api/markets"
                response = requests.get(url)
                data = response.json()
                for market in data['result']:
                    pair = f"{market['base']}/{market['quote']}"
                    all_pairs.add(pair)
            elif exchange_name == 'deribit':
                url = "https://www.deribit.com/api/v2/public/get_instruments?currency=USDT&expired=false"
                response = requests.get(url)
                data = response.json()
                for instrument in data['result']:
                    pair = f"{instrument['baseCurrency']}/{instrument['quoteCurrency']}"
                    all_pairs.add(pair)
            elif exchange_name == 'gateio':
                url = "https://api.gateio.ws/api/v4/futures/contracts"
                response = requests.get(url)
                data = response.json()
                for contract in data:
                    pair = f"{contract['base']}/{contract['quote']}"
                    all_pairs.add(pair)
        except Exception as e:
            logger.error(f"Ошибка при получении списка пар на бирже {exchange_name}: {e}")
    return list(all_pairs)

def update_exchange_configs(current_config):
    """
    Обновление конфигурационных файлов бирж.
    """
    # Пример: Обновление конфигураций бирж на основе новых данных
    updated_config = current_config.copy()
    # Здесь можно добавить логику обновления конфигураций
    return updated_config