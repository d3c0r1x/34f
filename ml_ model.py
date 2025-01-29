import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from config import config

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_data(pair):
    """
    Загрузка исторических данных для пары.
    """
    data = pd.read_csv(f'data/{pair}.csv')
    return data

def preprocess_data(data):
    """
    Предобработка данных.
    """
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    return data

def train_model(data):
    """
    Обучение модели машинного обучения.
    """
    features = data.drop(columns=['Close'])
    target = data['Close']

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    logger.info(f"Среднеквадратичная ошибка модели: {mse}")

    return model

def predict_prices(model, new_data):
    """
    Прогнозирование цен с помощью обученной модели.
    """
    predictions = model.predict(new_data)
    return predictions

if __name__ == "__main__":
    pair = 'BTC/USD'
    data = load_data(pair)
    data = preprocess_data(data)
    model = train_model(data)
    new_data = data.tail(10).drop(columns=['Close'])
    predictions = predict_prices(model, new_data)
    logger.info(f"Прогнозные цены для пары {pair}: {predictions}")