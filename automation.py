import logging
import time
import yaml
from config import config
from testing import run_tests
from core import update_exchange_configs

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_configurations():
    """
    Автоматическое обновление конфигурационных файлов.
    """
    try:
        with open('config.yaml', 'r') as file:
            current_config = yaml.safe_load(file)

        updated_config = update_exchange_configs(current_config)
        if updated_config != current_config:
            with open('config.yaml', 'w') as file:
                yaml.safe_dump(updated_config, file)
            logger.info("Конфигурационные файлы успешно обновлены.")
        else:
            logger.info("Конфигурационные файлы не требуют обновления.")
    except Exception as e:
        logger.error(f"Ошибка при обновлении конфигурационных файлов: {e}")

def run_periodic_tasks():
    """
    Выполнение периодических задач.
    """
    while True:
        logger.info("Запуск периодических задач...")
        update_configurations()
        run_tests()
        logger.info("Периодические задачи завершены.")
        time.sleep(config['automation_interval'])

if __name__ == "__main__":
    run_periodic_tasks()