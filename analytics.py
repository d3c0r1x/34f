import logging
import pandas as pd
import yfinance as yf
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.trend import SMAIndicator, MACD
from ta.volatility import BollingerBands
import requests
from config import config

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_historical_data(pair, period='1y', interval='1d'):
    """
    Получение исторических данных о ценах для пары.
    """
    ticker = f"{pair.replace('/', '')}.US"
    data = yf.download(ticker, period=period, interval=interval)
    return data

def calculate_indicators(data):
    """
    Вычисление технических индикаторов.
    """
    rsi = RSIIndicator(data['Close']).rsi()
    stoch = StochasticOscillator(data['High'], data['Low'], data['Close'])
    macd = MACD(data['Close'])
    bb = BollingerBands(data['Close'])

    data['RSI'] = rsi
    data['Stoch_K'] = stoch.stoch()
    data['Stoch_D'] = stoch.stoch_signal()
    data['MACD'] = macd.macd()
    data['MACD_Signal'] = macd.macd_signal()
    data['BB_High'] = bb.bollinger_hband()
    data['BB_Low'] = bb.bollinger_lband()

    return data

def analyze_liquidity(data):
    """
    Анализ ликвидности на основе объема торговли.
    """
    data['Liquidity'] = data['Volume'].rolling(window=10).mean()
    return data

def fetch_additional_data(pair):
    """
    Получение дополнительных данных (например, экономические индикаторы).
    """
    # Пример: Получение данных о валюте из API
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={pair.replace('/', '-')}&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        additional_data = {
            'coingecko_price': data.get(pair.replace('/', '-'), {}).get('usd', 0)
        }
        return additional_data
    except Exception as e:
        logger.error(f"Ошибка при получении дополнительных данных для пары {pair}: {e}")
        return {}

def generate_report(data, pair, additional_data):
    """
    Генерация отчета и графиков для анализа рынка.
    """
    report = {
        'Pair': pair,
        'Last_Close': data['Close'].iloc[-1],
        'RSI': data['RSI'].iloc[-1],
        'Stoch_K': data['Stoch_K'].iloc[-1],
        'Stoch_D': data['Stoch_D'].iloc[-1],
        'MACD': data['MACD'].iloc[-1],
        'MACD_Signal': data['MACD_Signal'].iloc[-1],
        'BB_High': data['BB_High'].iloc[-1],
        'BB_Low': data['BB_Low'].iloc[-1],
        'Liquidity': data['Liquidity'].iloc[-1],
        'Coingecko_Price': additional_data.get('coingecko_price', 0)
    }
    logger.info(f"Отчет для пары {pair}: {report}")
    return report

if __name__ == "__main__":
    pair = 'BTC/USD'
    data = get_historical_data(pair)
    data = calculate_indicators(data)
    data = analyze_liquidity(data)
    additional_data = fetch_additional_data(pair)
    report = generate_report(data, pair, additional_data)