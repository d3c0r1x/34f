import logging
from arbitrage import find_arbitrage_opportunities
from automation import run_periodic_tasks
from threading import Thread

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """
    Главная функция для запуска бота.
    """
    logger.info("Запуск бота...")

    # Запуск потока для поиска арбитражных возможностей
    arbitrage_thread = Thread(target=find_arbitrage_opportunities)
    arbitrage_thread.daemon = True
    arbitrage_thread.start()

    # Запуск потока для периодических задач
    automation_thread = Thread(target=run_periodic_tasks)
    automation_thread.daemon = True
    automation_thread.start()

    # Основной цикл бота
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем.")

if __name__ == "__main__":
    main()